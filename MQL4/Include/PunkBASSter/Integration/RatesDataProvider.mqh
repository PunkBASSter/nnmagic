//Scans for data updates and returns the latest
class CRatesDataProvider
{
private:
   
   string _symbol;
   ENUM_TIMEFRAMES _period;
   datetime _lastDate;
   bool _reSendLastBar;

public:
   
   int GetRatesUpdates(MqlRates &outBuf[], datetime endDate=0)
   {
      datetime latestBarToStartCopy = endDate;
      if(endDate == 0 || endDate < _lastDate) latestBarToStartCopy = TimeCurrent();
      
      int copied = CopyRates(_symbol, _period, latestBarToStartCopy, _lastDate, outBuf);
      
      _lastDate = MathMax(outBuf[0].time, outBuf[copied-_reSendLastBar].time);
      
      return copied;
   }
   
   int GetLastRates(MqlRates &outBuf[], int count=50)
   {
      return CopyRates(_symbol,_period,0,count,outBuf);
   }
   
   CRatesDataProvider(const string symbol, const ENUM_TIMEFRAMES period, const datetime startDate = D'01.01.2010', bool reSendLastBar=true)
   {
      _symbol = symbol;
      _period = period;
      _lastDate = startDate;
      _reSendLastBar = reSendLastBar;
   };
};