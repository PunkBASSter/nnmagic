//+------------------------------------------------------------------+
//|                                             DataToTextExport.mqh |
//|                                                      PunkBASSter |
//|                        https://www.mql5.com/en/users/punkbasster |
//+------------------------------------------------------------------+
#property copyright "PunkBASSter"
#property link      "https://www.mql5.com/en/users/punkbasster"
#property strict

#include "DataContracts.mqh"

string AddString(string name, string value, string signAfter=",")
{
   return StringFormat("\"%s\":\"%s\"%s",name,value,signAfter);
}
string AddInt(string name, long value, string signAfter=",")
{
   return StringFormat("\"%s\":%d%s",name,value,signAfter);
}
string AddFloat(string name, double value, string signAfter=",")
{
   return StringFormat("\"%s\":%f%s",name,value,signAfter);
}

//DEPRECATED
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

string RatesToJsonObject(MqlRates &rates)
{
   string result = "{";
   result += AddInt("timestamp", (int)rates.time);
   result += AddInt("time_current", (int)TimeCurrent()); //might be useless
   result += AddFloat("open", rates.open);
   result += AddFloat("high", rates.high);
   result += AddFloat("low", rates.low);
   result += AddFloat("close", rates.close);
   result += AddInt("tick_volume", rates.tick_volume);
   result += AddInt("spread", rates.spread);
   result += AddInt("real_volume", rates.real_volume,"}");
   return result;
}

string RatesArrayToJson(MqlRates &array[])
{
   int arrSize = ArraySize(array);
   string result = "\"rates\":[";
   
   int i;
   for (i=0; i< arrSize; i++)
   {
      result += RatesToJsonObject(array[i]);
      result += ",";
   }
   if(i>0)
      result = StringSubstr(result, 0, StringLen(result)-1); //removes last comma
   return result + "]";
}

string OrderToJsonObject(OrderItem &item)
{
   string result = "{";
   
   result += AddInt("command", item.command);
   result += AddFloat("open_price", item.open);
   result += AddFloat("stop_loss", item.stop_loss);
   result += AddFloat("take_profit", item.take_profit);
   result += AddFloat("lots", item.lots);
   result += AddInt("expiration_date", item.expiration);
   result += AddInt("ticket", item.ticket);
   result += AddInt("open_time", item.open_time,"}");
   return result;
}

string OrdersArrayToJson(OrderItem &array[])
{
   int arrSize = ArraySize(array);
   string result = "\"orders\":[";
   
   int i;
   for (i=0; i< arrSize; i++)
   {
      result += OrderToJsonObject(array[i]);
      result += ",";
   }
   if(i>0)
      result = StringSubstr(result, 0, StringLen(result)-1); //removes last comma
   return result + "]";
}