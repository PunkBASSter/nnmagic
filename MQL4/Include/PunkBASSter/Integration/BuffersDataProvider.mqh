#include "DataContracts.mqh"

typedef void (*TIndicatorInitStrategy) (void);

//Scans for data updates and returns the latest
class CBuffersDataProvider
{
private:
   
   string _symbol;
   ENUM_TIMEFRAMES _period;
   datetime _lastDate;
   int _latestBarShift;

//Assigned in SetBuffersConfig(...)
   BufferDescriptor _buffersConfig[];
   
//Assigned in 
   TIndicatorInitStrategy _indicatorInitFuncPtr;

protected:
   
   int GetRatesUpdates(MqlRates &outBuf[], int chunkSize = 100)
   {
      int oneBarTimeSpan = PeriodSeconds(_period);
      datetime latestBarToStartCopy = _lastDate + chunkSize*oneBarTimeSpan;//TimeCurrent()-_latestBarShift*PeriodSeconds(_period);
      int barsToCopy = (int)MathMin((TimeCurrent()-_lastDate)/oneBarTimeSpan, chunkSize);
      int copied = CopyRates(_symbol, _period, latestBarToStartCopy, _lastDate, outBuf);
      
      _lastDate = MathMax(outBuf[0].time, outBuf[copied-1].time);
      
      return copied;
   }
   
   int GetIndicatorsDataByTime(datetime const time, BufferDescriptor const &bufDescriptors[], BufferNameValue &bufValues[])
   {
      int copyErrors = 0;
      
      int total = ArraySize(bufDescriptors);
      ArrayResize(bufValues,total);
      for (int i=0; i<total; i++)
      {
         double value[1];
         int copied = CopyBuffer(bufDescriptors[i].handle,bufDescriptors[i].bufNum,time+PeriodSeconds(_period)-10,1,value);
         datetime tmpTime[1];
         CopyTime(_symbol,_period,time+PeriodSeconds(_period)-10,1,tmpTime);
         
         bufValues[i].name = bufDescriptors[i].name; //to control possible errors in buffers copying by name-to-name mapping
         bufValues[i].value=value[0];
         bufValues[i].time=tmpTime[0];
         if (copied < 1)
         {
            copyErrors++;
            bufValues[i].value=EMPTY_VALUE;
         }
      }
      
      return copyErrors;
   }
   
   DataItem GetDataItem(MqlRates &rates)
   {
      DataItem res;
      res.symbol = _symbol;
      res.period = _period;
      res.timestamp = (int)rates.time;
      //res.time_current = (int)TimeCurrent();
      res.open = rates.open;
      res.high = rates.high;
      res.low = rates.low;
      res.close = rates.close;
      res.tick_volume = rates.tick_volume;
      res.spread = rates.spread;
      res.real_volume = rates.real_volume;
      
      int errors = GetIndicatorsDataByTime(rates.time, _buffersConfig, res.buffers);
      if (errors > 0)
      {
         Print("Detected indicator buffers copying errors for date "+rates.time);
      }
      
      return res;
   }

public:

   //CBuffersDataProvider()
   //{
   //   _symbol = Symbol();
   //   _period = Period();
   //   _lastDate = D'01.01.2010';
   //   _latestBarShift = 0;
   //};

   CBuffersDataProvider(const string symbol, const ENUM_TIMEFRAMES period, const datetime startDate = D'01.01.2010', const int latestBarShift = 0)
   {
      _symbol = symbol;
      _period = period;
      _lastDate = startDate;
      _latestBarShift = latestBarShift;
   };
   
   int GetDataItems(DataItem &outDataItems[])
   {
      MqlRates newRates[];
      int ratesCount = GetRatesUpdates(newRates);
      ArrayResize(outDataItems, ratesCount);
      
      for(int i = 0; i < ratesCount; i++)
      {
         outDataItems[i]=GetDataItem(newRates[i]);
      }
      
      return ratesCount;
   }
   
   //Calls an injected initialization strategy or can be overridden in inherited classes
   virtual void InitIndicators()
   {
      if (_indicatorInitFuncPtr != NULL)
         _indicatorInitFuncPtr();
   }

   
//Field getters/setters:

   void SetIndicatorInitStrategy(TIndicatorInitStrategy initStrategy){ _indicatorInitFuncPtr = initStrategy; }

   void SetBuffersConfig(BufferDescriptor &buffersConfig[])
   {
      int size = ArraySize(buffersConfig);
      ArrayResize(_buffersConfig,size);
      for (int i = 0; i< size; i++)
      {
         _buffersConfig[i]=buffersConfig[i];
      }
   }
   
};