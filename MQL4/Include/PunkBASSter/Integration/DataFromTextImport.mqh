//+------------------------------------------------------------------+
//|                                           DataFromTextImport.mqh |
//|                                                      PunkBASSter |
//|                        https://www.mql5.com/en/users/punkbasster |
//+------------------------------------------------------------------+
#property copyright "PunkBASSter"
#property link      "https://www.mql5.com/en/users/punkbasster"
#property strict

#include "DataContracts.mqh"

#define ORDER_COMMAND "command"
#define ORDER_OPEN_PRICE "open_price"
#define ORDER_STOP_LOSS "stop_loss"
#define ORDER_TAKE_PROFIT "take_profit"
#define ORDER_LOTS "lots"
#define ORDER_EXPIRATION "expiration_date"
#define ORDER_TICKET "ticket"
#define ORDER_SYMBOL "symbol"

string TrimStr(string str)
{
   return StringTrimRight(StringTrimLeft(str));
}

OrderItem ParseOrderCsvString(string rawText, char sep = ',')
{
   string splitted[];
   StringSplit(rawText, sep, splitted);
   OrderItem item;
   item.command = StrToInteger(splitted[0]);
   item.open = StrToDouble(splitted[1]);
   item.stop_loss = StrToDouble(splitted[2]);
   item.take_profit = StrToDouble(splitted[3]);
   item.lots = StrToDouble(splitted[4]);
   item.expiration = (datetime)splitted[5];
   return item;
}

int ParseOrdersCsvToArray(OrderItem &outOrders[], string rawText,char lineSep = '\n', char colSep = ',')
{
   string rows[];
   StringSplit(TrimStr(rawText), lineSep, rows);
   int rowsTotal = ArraySize(rows)-1; //Rows with values (without header)
   
   if(rowsTotal<1) //only header or nothing is passed
      return 0;
   
   string headerColumns[];
   StringSplit(TrimStr(rows[0]), colSep, headerColumns);
   int columnsTotal = ArraySize(headerColumns);
   
   int count = 0;
   ArrayResize(outOrders,rowsTotal);
   for(int i = 1; i < rowsTotal + 1; i++) //from 1 to the end
   {
      string row = TrimStr(rows[i]);
      string columns[];
      StringSplit(TrimStr(row), colSep, columns);
      
      if (row=="" || row==NULL)
            continue;
      
      OrderItem item;
      item.command = -1;
      
      for (int j = 0; j<ArraySize(columns); j++)
      {
         string column = TrimStr(columns[j]);
         if (column=="" || column==NULL)
            continue;
      
         string key = TrimStr(headerColumns[j]);
      
         if(key == ORDER_TICKET)//exceptional case for ticket: 0 is a valid value for it.
         {
            string val = column == "" ? "-1" : column;
            item.ticket = StrToInteger(val);
            continue;
         }
      
         string value = column == "" ? "0" : columns[j];
         if(key == ORDER_COMMAND){ item.command = StrToInteger(value); continue; }
         if(key == ORDER_OPEN_PRICE){ item.open = StrToDouble(value); continue; }      
         if(key == ORDER_STOP_LOSS){ item.stop_loss = StrToDouble(value); continue; }      
         if(key == ORDER_TAKE_PROFIT){ item.take_profit = StrToDouble(value); continue; }      
         if(key == ORDER_LOTS){ item.lots = StrToDouble(value); continue; }      
         if(key == ORDER_EXPIRATION){ item.expiration = (datetime)value; continue; }
         if(key == ORDER_SYMBOL){ item.symbol = value != NULL ? value : Symbol(); continue; }
      }
      
      outOrders[count]=item;
      count++;
   }
   
   ArrayResize(outOrders,count);
   return count;
}

