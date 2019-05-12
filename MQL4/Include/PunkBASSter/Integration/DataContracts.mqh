//+ from OP_BUY to OP_SELLSTOP
#define OP_UPDATE 8
#define OP_REMOVE 9
#define OP_PASS 10

struct OrderItem
{
   int command;
   double open;
   double stop_loss;
   double take_profit;
   double lots;
   datetime expiration;
   int ticket;
   datetime open_time;
   string symbol;
};