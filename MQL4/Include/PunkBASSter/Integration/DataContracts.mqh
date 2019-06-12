//+ from OP_BUY to OP_SELLSTOP
#define OP_UPDATE 8
#define OP_REMOVE 9
#define OP_PASS 10

#define BOT_STATE_INIT "INIT"
#define BOT_STATE_INIT_COMPLETE "INIT_COMPLETE"
#define BOT_STATE_TICK "TICK"
#define BOT_STATE_ORDERS "ORDERS"
#define SUCCESS_RESULT "OK"
#define ERROR_RESULT "ERROR"

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