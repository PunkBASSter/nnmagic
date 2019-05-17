//+------------------------------------------------------------------+
//|                                                        Trade.mqh |
//|                                                      PunkBASSter |
//|                        https://www.mql5.com/en/users/punkbasster |
//+------------------------------------------------------------------+
#property copyright "PunkBASSter"
#property link      "https://www.mql5.com/en/users/punkbasster"
#property strict

#include <PunkBASSter/Integration/DataContracts.mqh>

class CTrade
{
   private:
      int _slippage;
      int _magic;
      bool _singleOrder;
      bool CheckPriceLevelAssigned(double priceLevel)
      {
         return MathIsValidNumber(priceLevel) && priceLevel > 0 && priceLevel < 9999999999; //No MAX_DOUBLE constant in MQL4 :'(
      }
      
   public:
      
      OrderItem NormalizeItem(OrderItem &item)
      {
         int digits = (int)MarketInfo(item.symbol, MODE_DIGITS);
         item.lots = NormalizeDouble(item.lots,2);
         item.open = NormalizeDouble(item.open,digits);
         item.stop_loss = NormalizeDouble(item.stop_loss,digits);
         item.take_profit = NormalizeDouble(item.take_profit,digits);
         return item;
      }
      
      int CreateOrder(OrderItem &item)
      {
         int orderCmd = item.command;
         
         item = NormalizeItem(item);
         if(!CheckPriceLevelAssigned(item.open))
         {
            if(orderCmd == OP_BUY)
               item.open = MarketInfo(item.symbol, MODE_ASK);
            if(orderCmd == OP_SELL)
               item.open = MarketInfo(item.symbol, MODE_BID);
         }
         
         return OrderSend(item.symbol,orderCmd,item.lots,item.open,_slippage,item.stop_loss,item.take_profit,NULL,_magic,item.expiration,clrGreen);
      }
      
      bool UpdateOrder(OrderItem const &item)
      {
         if(!OrderSelect(item.ticket,SELECT_BY_TICKET,MODE_TRADES))
         {
            PrintFormat("WARNING! Requested update of not existing order #%d.", item.ticket);
            return true;
         }
         
         int ticket = item.ticket;
         double price = CheckPriceLevelAssigned(item.open) ? item.open : OrderOpenPrice();
         double sl = CheckPriceLevelAssigned(item.stop_loss) ? item.stop_loss : OrderStopLoss();
         double tp = CheckPriceLevelAssigned(item.take_profit) ? item.take_profit : OrderTakeProfit();
         datetime expiration = item.expiration > 0 ? item.expiration : OrderExpiration();
         
         int digits = (int)MarketInfo(item.symbol, MODE_DIGITS);
         return OrderModify(ticket,NormalizeDouble(price,digits),NormalizeDouble(sl,digits),NormalizeDouble(tp,digits),expiration, clrBlue);
      }
      
      bool RemoveOrder(OrderItem const &item)
      {
         if(!OrderSelect(item.ticket,SELECT_BY_TICKET,MODE_TRADES))
         {
            PrintFormat("WARNING! Requested removal of not existing order #%d.", item.ticket);
            return true;
         }
         
         if(OrderDelete(item.ticket, clrRed))
            return true;
         
         double closePrice = OrderType() == OP_BUY 
            ? MarketInfo(item.symbol, MODE_BID)
            : MarketInfo(item.symbol, MODE_ASK);
         
         int digits = (int)MarketInfo(item.symbol, MODE_DIGITS);
         return OrderClose(item.ticket,OrderLots(),NormalizeDouble(closePrice,digits),_slippage, clrRed);
      }
   
      int GetOwnActiveOrders(OrderItem &outBuf[])
      {
         for(int i=0; i<OrdersTotal(); i++)
         {
            int currentSize = ArraySize(outBuf);
            
            if(OrderSelect(i,SELECT_BY_POS,MODE_TRADES))
            {
               if(OrderMagicNumber()==_magic)
               {
                  ArrayResize(outBuf,currentSize+1,currentSize+10);
                  OrderItem item;
                  item.command = OrderType();
                  item.symbol = OrderSymbol();
                  item.lots = OrderLots();
                  item.open = OrderOpenPrice();
                  item.stop_loss = OrderStopLoss();
                  item.take_profit = OrderTakeProfit();
                  item.expiration = OrderExpiration();
                  item.ticket = OrderTicket();
                  item.open_time = OrderOpenTime();
                  outBuf[currentSize]= item;
               }
            }
         }
         return ArraySize(outBuf);
      }
   
      CTrade(int magic, int slippage=20)
      {
         _magic = magic;
         _slippage = slippage;
      }
};
