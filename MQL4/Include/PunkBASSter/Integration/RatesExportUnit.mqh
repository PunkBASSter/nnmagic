//+------------------------------------------------------------------+
//|                                                   ExportUnit.mqh |
//|                                                      PunkBASSter |
//|                        https://www.mql5.com/en/users/punkbasster |
//+------------------------------------------------------------------+
#property copyright "PunkBASSter"
#property link      "https://www.mql5.com/en/users/punkbasster"
#property version   "1.00"
#property strict

#include <PunkBASSter/Integration/RatesDataProvider.mqh>
#include <PunkBASSter/Integration/DataToTextExport.mqh>
#include <PunkBASSter/Integration/DataFromTextImport.mqh>
#include <PunkBASSter/Integration/TextIO.mqh>
#include <PunkBASSter/Integration/DataContracts.mqh>
#include <PunkBASSter/Common/Trade.mqh>


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
class CRatesExportUnit
  {
private:
   string _symbol;
   ENUM_TIMEFRAMES _period;
   datetime _startDate;
   CRatesDataProvider *_ratesProvider;
   CTextIO *_textIo;
   int _chunkSize;

public:
                     CRatesExportUnit(CTextIO *textIo, datetime startDate, string symbol=NULL, int period=0, int chunkSize=100);
                    ~CRatesExportUnit();
                    string ExportRates(string state);
                    string SendState(string state);
  };
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
CRatesExportUnit::CRatesExportUnit(CTextIO *textIo, datetime startDate, string symbol=NULL, int period=0, int chunkSize=100)
  {
     if(symbol==NULL)_symbol=Symbol();
     else _symbol = symbol;
     if(period==0)_period=(ENUM_TIMEFRAMES)Period();
     else _period = (ENUM_TIMEFRAMES)period;
     _startDate = startDate;
     _ratesProvider = new CRatesDataProvider(_symbol,_period,_startDate);
     _chunkSize = chunkSize;
     _textIo = textIo;
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
CRatesExportUnit::~CRatesExportUnit()
  {
   delete _ratesProvider;
  }
//+------------------------------------------------------------------+

string CRatesExportUnit::ExportRates(string state)
{
   string response = ERROR_RESULT;

   MqlRates rates[];
   int copied = _ratesProvider.GetRatesUpdates(rates);
   for(int chunkStart = 0; chunkStart < copied; chunkStart+=_chunkSize)
   {
      MqlRates chunk[];
      int chunkCopied = ArrayCopy(chunk,rates,0,chunkStart,_chunkSize);
      string jsonChunk = "{" +
         AddString("state",state) +
         AddString("symbol",_symbol) +
         AddInt("timeframe",_period) +
         //AddInt("tf_seconds",PeriodSeconds(_period)) +
         AddInt("timestamp",(int)TimeCurrent()) +
         AddInt("size",ArraySize(chunk)) +
         RatesArrayToJson(chunk)+
      "}";
      response = _textIo.ExportDataGetTrade(jsonChunk);
      
      if (response != SUCCESS_RESULT)
      {
         Print("Sent chunk: ", jsonChunk);
         PrintFormat("Sent chunk from %d. Response \"%s\" received.", chunkStart, response);
      }
   }
   return response;
}

string CRatesExportUnit::SendState(string state)
{
   return _textIo.ExportDataGetTrade("{"+AddString("state",state)+AddString("symbol",_symbol)+AddInt("timeframe",_period,"")+"}");
}