#include "DataContracts.mqh"

string AddString(string name, string value)
{
   return StringFormat("\"%s\":\"%s\",",name,value);
}
string AddInt(string name, long value)
{
   return StringFormat("\"%s\":%d,",name,value);
}
string AddFloat(string name, double value)
{
   return StringFormat("\"%s\":%f,",name,value);
}

string RatesToCsv(MqlRates &rates[])
{
   string result = "timestamp,open,high,low,close,tick_volume,spread,real_volume\n";
   for(int i=0; i< ArraySize(rates); i++)
   {
      string item = StringFormat("%d,%f,%f,%f,%f,%d,%d,%d\r\n",
         (int)rates[i].time, rates[i].open, rates[i].high, rates[i].low, rates[i].close, rates[i].tick_volume, rates[i].spread, rates[i].real_volume);
      result += item;
   }
   return result;
}

string DataItemToJson(DataItem &dataItem)
{
   string result = "{";
   
   result += AddString("symbol",dataItem.symbol);
   result += AddString("period",EnumToString(dataItem.period));
   result += AddInt("timestamp", (int)dataItem.timestamp);
   result += AddInt("time_current", (int)TimeCurrent());
   result += AddFloat("open", dataItem.open);
   result += AddFloat("high", dataItem.high);
   result += AddFloat("low", dataItem.low);
   result += AddFloat("close", dataItem.close);
   result += AddInt("tick_volume", dataItem.tick_volume);
   result += AddInt("spread", dataItem.spread);
   result += AddInt("real_volume", dataItem.real_volume);
   
   for (int i=0; i<ArraySize(dataItem.buffers); i++)
   {
      result += AddFloat(dataItem.buffers[i].name, dataItem.buffers[i].value);
   }
   
   //remove last space and comma
   result = StringSubstr(result, 0, StringLen(result)-1);
   return result + "}";
}

string DataItemsToJson(DataItem &dataItems[])
{
   int arrSize = ArraySize(dataItems);
   string result = "{";
   
   result += AddInt("size",arrSize);
   result += "\"data\":[";
   
   for (int i=0; i< arrSize; i++)
   {
      result += DataItemToJson(dataItems[i]);
      result += ",";
   }
   
   result = StringSubstr(result, 0, StringLen(result)-1); //removes last comma
   return result + "]}";
}


string RatesToJsonObject(MqlRates &rates)
{
   string result = "{";
   
   result += AddInt("timestamp", (int)rates.time);
   result += AddInt("time_current", (int)TimeCurrent());
   result += AddFloat("open", rates.open);
   result += AddFloat("high", rates.high);
   result += AddFloat("low", rates.low);
   result += AddFloat("close", rates.close);
   result += AddInt("tick_volume", rates.tick_volume);
   result += AddInt("spread", rates.spread);
   result += AddInt("real_volume", rates.real_volume);
   
   //remove last space and comma
   result = StringSubstr(result, 0, StringLen(result)-1);
   return result + "}";
}

string RatesArrayToJson(MqlRates &array[])
{
   int arrSize = ArraySize(array);
   string result = "\"data\":[";
   
   for (int i=0; i< arrSize; i++)
   {
      result += RatesToJsonObject(array[i]);
      result += ",";
   }
   
   result = StringSubstr(result, 0, StringLen(result)-1); //removes last comma
   return result + "]";
}


//String parsing import data funcs
OrderItem ParseOrderCsvString(string rawText)
{
   string splitted[];
   StringSplit(rawText, ',', splitted);
   OrderItem item;
   item.type = splitted[0];
   item.open = StrToDouble(splitted[1]);
   item.stop_loss = StrToDouble(splitted[2]);
   item.take_profit = StrToDouble(splitted[3]);
   item.lots = StrToDouble(splitted[4]);
   item.expiration = (datetime)splitted[5];
   return item;
}

OrderItem ParseOrderKeyValueCsvString(string rawText)
{
   OrderItem item;
   
   string splittedPairs[];
   int pairs = StringSplit(rawText, ',', splittedPairs);
   
   for (int i = 0; i<pairs; i++)
   {
      string keyValuePair[];
      int len = StringSplit(splittedPairs[i], ':', keyValuePair);
      if (len != 2) continue;
      
      string key = keyValuePair[0];
      string value = keyValuePair[1] == "" ? "0" : keyValuePair[1];
      if (key == OrderTypeStr){ item.type = value; continue; }
      if (key == OrderOpenPriceStr){ item.open = StrToDouble(value); continue; }      
      if (key == OrderStopLossStr){ item.stop_loss = StrToDouble(value); continue; }      
      if (key == OrderTakeProfitStr){ item.take_profit = StrToDouble(value); continue; }      
      if (key == OrderLotsStr){ item.lots = StrToDouble(value); continue; }      
      if (key == OrderExpirationStr){ item.expiration = (datetime)value; continue; }      
   }
   
   return item;
}