//+------------------------------------------------------------------+
//|                                                DzzDataExport.mq4 |
//|                        Copyright 2017, MetaQuotes Software Corp. |
//|                        https://www.mql5.com/en/users/punkbasster |
//+------------------------------------------------------------------+
#property copyright "Copyright 2017, MetaQuotes Software Corp."
#property link      "https://www.mql5.com/en/users/punkbasster"
#property version   "1.00"
#property script_show_inputs

#include <Object.mqh>
#include <PunkBASSter/Integration/RatesDataProvider.mqh>

//--- input parameters
input string   OutputFileNameBase = "";
input datetime StartDate = D'01.01.2010';
input datetime EndDate = 0; //TimeCurrent() is taken if 0 or less than StartDate

void OnStart()
{
   CRatesDataProvider *provider = new CRatesDataProvider(Symbol(),(ENUM_TIMEFRAMES)Period(),StartDate);
   
   MqlRates rates[];
   int copied = provider.GetRatesUpdates(rates, EndDate);
   
   int fileHandle = OpenFile();
   
   //write header
   FileWriteString(fileHandle, "timestamp,open,high,low,close,tick_volume,spread,real_volume\n");
   
   //write content ordered by ascending date
   for(int i=0; i<=copied-1; i++)
   {
      string item = StringFormat("%d,%f,%f,%f,%f,%d,%d,%d\r\n",
         (int)rates[i].time, rates[i].open, rates[i].high, rates[i].low, rates[i].close, rates[i].tick_volume, rates[i].spread, rates[i].real_volume);
      FileWriteString(fileHandle,item);
   }

   delete provider;
   FileClose(fileHandle);
}

int OpenFile()
{
   string fileName = OutputFileNameBase + Symbol() + "_" + EnumToString((ENUM_TIMEFRAMES)Period()) + ".csv";
   
   int handle = FileOpen(fileName,FILE_WRITE|FILE_COMMON|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      PrintFormat("Failed to open file \"%s\", error code: %d.",fileName,_LastError);
   }
   return handle;
}