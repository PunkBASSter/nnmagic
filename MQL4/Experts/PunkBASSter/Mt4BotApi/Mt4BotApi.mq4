//+------------------------------------------------------------------+
//|                                                     MtBotApi.mq5 |
//|                                     Copyright 2018, PunkBASSter. |
//|                        https://www.mql5.com/en/users/punkbasster |
//+------------------------------------------------------------------+
//#include "BuffersDataProvider.mqh"
#include <PunkBASSter/Integration/RatesExportUnit.mqh>
#include <PunkBASSter/Integration/DataToTextExport.mqh>
#include <PunkBASSter/Integration/DataFromTextImport.mqh>
#include <PunkBASSter/Integration/TextIO.mqh>
#include <PunkBASSter/Common/Trade.mqh>

//input string ControlPipeName = "ControlPipe"; //Used to request for data pipes.
input string DataPipeName = "MyDataPipe";
input datetime HistoryStart = D'2016.01.01';
input int ChunkSize = 100;
input int InpMagic = 123123;

//CRatesDataProvider *ratesProvider;
CTextIO *dataTextIO;
CTrade *trade;
CRatesExportUnit *hoursExport;
CRatesExportUnit *daysExport;

//int _ticket;

string GenerateUniquePipeName()
{
   return StringFormat("DataPipe_%d", rand());
}

/*void PrintData()
{
   MqlRates rates[];
   int total = ratesProvider.GetRatesUpdates(rates);
   
   for (int i=0; i<total; i++)
   {
      Print(__FUNCTION__ + " : " +RatesToJsonObject(rates[i]));
   }
}

string ExportRates(string state, string symbol = NULL, ENUM_TIMEFRAMES period = 0)
{
   //WARNING! Symbol and Period must be synchronized with dataTextIO!
   //TODO encapsulate all export infrastructure in 1 class with common settings.
   string response = ERROR_RESULT;
   if(symbol==NULL)symbol=Symbol();
   if(period==0)period=(ENUM_TIMEFRAMES)Period();

   MqlRates rates[];
   int copied = ratesProvider.GetRatesUpdates(rates);
   for(int chunkStart = 0; chunkStart < copied; chunkStart+=ChunkSize)
   {
      MqlRates chunk[];
      int chunkCopied = ArrayCopy(chunk,rates,0,chunkStart,ChunkSize);
      string jsonChunk = "{" +
         AddString("state",state) +
         AddString("symbol",symbol) +
         AddInt("timeframe",period) +
         AddInt("tf_seconds",PeriodSeconds(period)) +
         AddInt("timestamp",(int)TimeCurrent()) +
         AddInt("size",ArraySize(chunk)) +
         RatesArrayToJson(chunk)+
      "}";
      response = dataTextIO.ExportDataGetTrade(jsonChunk);
      
      if (response != SUCCESS_RESULT)
      {
         Print("Sent chunk: ", jsonChunk);
         PrintFormat("Sent chunk from %d. Response \"%s\" received.", chunkStart, response);
      }
   }
   return response;
}

string SendState(string state, string symbol = NULL, ENUM_TIMEFRAMES period = 0)
{
   if(symbol==NULL)symbol=Symbol();
   if(period==0)period=(ENUM_TIMEFRAMES)Period();
   return dataTextIO.ExportDataGetTrade("{"+AddString("state",state)+AddString("symbol",symbol)+AddInt("timeframe",period,"")+"}");
}
*/

string ExportOrders(string state = BOT_STATE_ORDERS)
{
   string response = ERROR_RESULT;
   
   OrderItem orders[];
   trade.GetOwnActiveOrders(orders);
   string msg = "{" +
   AddString("state",state) + 
      OrdersArrayToJson(orders)+
   "}";

   response = dataTextIO.ExportDataGetTrade(msg);
         
   if (response != SUCCESS_RESULT)
   {
      PrintFormat("Sent active orders with Magic: %d for %s. Response \"%s\" received.", InpMagic, Symbol(), response);
   }
   return response;
}

bool ProcessOrderItems(OrderItem &orderItems[])
{
   int total = ArraySize(orderItems);
   int successResultCount = 0;
   for (int i = 0; i<total; i++)
   {
      if(orderItems[i].command>=OP_BUY && orderItems[i].command<=OP_SELLSTOP)
      {
         successResultCount += (-1 < trade.CreateOrder(orderItems[i]));
         continue;
      }
      if(orderItems[i].command == OP_UPDATE)
      {
         successResultCount += trade.UpdateOrder(orderItems[i]);
         continue;
      }
      if(orderItems[i].command == OP_REMOVE)
      {
         successResultCount += trade.RemoveOrder(orderItems[i]);
         continue;
      }
   }
   return successResultCount == total;
}

int OnInit()
{
   dataTextIO = new CTextIO;
   dataTextIO.Open(StringFormat("\\\\.\\pipe\\%s", DataPipeName));  
   hoursExport = new CRatesExportUnit(dataTextIO,HistoryStart,Symbol(),PERIOD_H1);
   daysExport = new CRatesExportUnit(dataTextIO,HistoryStart,Symbol(),PERIOD_D1);
   //ratesProvider = new CRatesDataProvider(Symbol(), (ENUM_TIMEFRAMES)Period(), HistoryStart);   
   trade = new CTrade(InpMagic,20);
   
   string result = hoursExport.ExportRates(BOT_STATE_INIT);
   Print("Init result: "+result);
   if(result != SUCCESS_RESULT)
      return(INIT_FAILED);
   
   result = daysExport.ExportRates(BOT_STATE_INIT);
   Print("Init result: "+result);
   if(result != SUCCESS_RESULT)
      return(INIT_FAILED);
      
   result = hoursExport.SendState(BOT_STATE_INIT_COMPLETE);
   if(result != SUCCESS_RESULT)
      return(INIT_FAILED);

   //OnTick();
   ExportOrders();
   
   return(INIT_SUCCEEDED);
}

void OnTick()
{
   ExportOrders();
   string response = daysExport.ExportRates(BOT_STATE_TICK);
   if (StringLen(response)<10) //short status message TODO PROCESS ERRORS
      return;

   response = hoursExport.ExportRates(BOT_STATE_TICK);
   if (StringLen(response)<10) //short status message TODO PROCESS ERRORS
      return;

   OrderItem orderItems[];
   int orders = ParseOrdersCsvToArray(orderItems, response); //only 1 order is currently supported
   
   bool res = ProcessOrderItems(orderItems);
   if (!res)
      PrintFormat("Unable to open order(s), last error: %d", GetLastError());
   
   ExportOrders();
}

void OnDeinit(const int reason)
{
   //delete ratesProvider;
   dataTextIO.Close();
   delete dataTextIO;
}

void OnTrade()
{
}

void OnBookEvent(const string &symbol)
{
}