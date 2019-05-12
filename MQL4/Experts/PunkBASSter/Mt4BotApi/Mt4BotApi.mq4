//+------------------------------------------------------------------+
//|                                                     MtBotApi.mq5 |
//|                                     Copyright 2018, PunkBASSter. |
//|                        https://www.mql5.com/en/users/punkbasster |
//+------------------------------------------------------------------+
//#include "BuffersDataProvider.mqh"
#include <PunkBASSter/Integration/RatesDataProvider.mqh>
#include <PunkBASSter/Integration/DataToTextExport.mqh>
#include <PunkBASSter/Integration/DataFromTextImport.mqh>
#include <PunkBASSter/Integration/TextIO.mqh>
#include <PunkBASSter/Common/Trade.mqh>

//input string ControlPipeName = "ControlPipe"; //Used to request for data pipes.
input string DataPipeName = "MyDataPipe";
input datetime HistoryStart = D'2008.11.19';
input int ChunkSize = 100;
input int InpMagic = 123124;

#define BOT_STATE_INIT "INIT"
#define BOT_STATE_INIT_COMPLETE "INIT_COMPLETE"
#define BOT_STATE_TICK "TICK"
#define BOT_STATE_ORDERS "ORDERS"
#define SUCCESS_RESULT "OK"
#define ERROR_RESULT "ERROR"

CRatesDataProvider *ratesProvider;
CTextIO dataTextIO;
CTrade *trade;
int _ticket;

string GenerateUniquePipeName()
{
   return StringFormat("DataPipe_%d", rand());
}

void PrintData()
{
   MqlRates rates[];
   int total = ratesProvider.GetRatesUpdates(rates);
   
   for (int i=0; i<total; i++)
   {
      Print(__FUNCTION__ + " : " +RatesToJsonObject(rates[i]));
   }
}

string ExportRates(string state, string symbol = NULL)
{
   string response = ERROR_RESULT;
   if(symbol==NULL)symbol=Symbol();

   MqlRates rates[];
   int copied = ratesProvider.GetRatesUpdates(rates);
   for(int chunkStart = 0; chunkStart < copied; chunkStart+=ChunkSize)
   {
      MqlRates chunk[];
      int chunkCopied = ArrayCopy(chunk,rates,0,chunkStart,ChunkSize);
      string jsonChunk = "{" +
         AddString("state",state) +
         AddString("symbol",symbol) +
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

string SendState(string state, string symbol = NULL)
{
   if(symbol==NULL)symbol=Symbol();
   return dataTextIO.ExportDataGetTrade("{"+AddString("state",state)+AddString("symbol",symbol,"")+"}");
}

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

int OnInit()
{
   dataTextIO.Open(StringFormat("\\\\.\\pipe\\%s", DataPipeName));  
   ratesProvider = new CRatesDataProvider(Symbol(), (ENUM_TIMEFRAMES)Period(), HistoryStart);   
   trade = new CTrade(InpMagic,20);
   
   string result = ExportRates(BOT_STATE_INIT);
   Print("Init result: "+result);
   
   if(result != SUCCESS_RESULT)
      //todo log
      return(INIT_FAILED);
      
   result = SendState(BOT_STATE_INIT_COMPLETE);
   if(result != SUCCESS_RESULT)
      return(INIT_FAILED);

   OnTick();
   
   return(INIT_SUCCEEDED);
}

void OnTick()
{
   ExportOrders();
   string response = ExportRates(BOT_STATE_TICK);
   
   if (StringLen(response)<10) //short status message TODO PROCESS ERRORS
      return;

   OrderItem orderItems[];
   int orders = ParseOrdersCsvToArray(orderItems, response); //only 1 order is currently supported
   
   for (int i = 0; i<orders; i++)
   {
      if(orderItems[i].command>=OP_BUY && orderItems[i].command<=OP_SELLSTOP)
      {
         trade.CreateOrder(orderItems[i]);
         continue;
      }
      if(orderItems[i].command == OP_UPDATE)
      {
         trade.UpdateOrder(orderItems[i]);
         continue;
      }
      if(orderItems[i].command == OP_REMOVE)
      {
         trade.RemoveOrder(orderItems[i]);
         continue;
      }
   }
   
   ExportOrders();
}

void OnDeinit(const int reason)
{
   delete ratesProvider;
   dataTextIO.Close();
}

void OnTrade()
{
}

void OnBookEvent(const string &symbol)
{
}