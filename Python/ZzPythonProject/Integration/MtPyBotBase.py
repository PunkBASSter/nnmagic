import json
import pandas as pd
import Mt5PipeConnector.PipeServer as pipe

BOT_STATE_INIT = "INIT"
BOT_STATE_TICK = "TICK"
BOT_STATE_ORDERS = "ORDERS"
RESULT_SUCCESS = "OK"
RESULT_ERROR = "ERROR"

OP_BUY = 0
OP_SELL = 1
OP_BUYLIMIT = 2
OP_SELLLIMIT = 3
OP_BUYSTOP = 4
OP_SELLSTOP = 5
OP_UPDATE = 8
OP_REMOVE = 9
OP_NONE = 1000

class OrderModel:
    command: int
    open_price: float
    stop_loss: float
    take_profit: float
    lots: float
    expiration_date = 0
    ticket = -1

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return f'Type:{self.command},OpenPrice:{self.open_price},StopLoss:{self.stop_loss},TakeProfit:{self.take_profit}' \
            f',Lots:{self.lots},ExpirationDate:{self.expiration_date},Ticket:{self.ticket}'

    def to_df(self) -> pd.DataFrame:
        d = self.__dict__
        df =  pd.DataFrame([self.__dict__])
        return df


class MtPyBotBase:
    """Encapsulates basic API calls and structure of MT bot business logic"""
    """Response format; Traded assets; Pipe management mb; """

    _order_fields = ["command", "open_price", "stop_loss", "take_profit", "lots", "expiration_date", "ticket", "open_time"]
    _response_format: str
    _data: pd.DataFrame
    _state: str
    _active_orders: pd.DataFrame

    def __init__(self, response_format=""):
        self._data = pd.DataFrame()
        self._state = BOT_STATE_INIT
        self._response_format = response_format
        self._active_orders = pd.DataFrame() #should contain extended info about existing orders
        self._orders_to_open = pd.DataFrame(columns=self._order_fields[0:7]) #should contain short info just to open order

    def process_json_data(self, data_updates: str) -> str:

        json_dict = json.loads(data_updates)
        self._state = json_dict["state"]

        if self._state == BOT_STATE_INIT:
            try:
                temp_df = pd.DataFrame(json_dict["data"])
                temp_df = temp_df.set_index("timestamp")
                self._data = pd.concat([self._data, temp_df])
                return RESULT_SUCCESS
            except Exception as e:
                return RESULT_ERROR + "_" + e.__str__()

        if self._state == BOT_STATE_TICK:
            self._data = self._data[~self._data.index.duplicated(keep='last')]
            result = self.on_tick_handler()
            return result

        if self._state == BOT_STATE_ORDERS:
            try:
                orders_df = pd.DataFrame(json_dict["orders"])
                #orders_df = orders_df.set_index("ticket")
                prev_orders = self._active_orders
                if not orders_df.equals(prev_orders):
                    self.on_orders_changed_handler(prev_orders, orders_df)
                self._active_orders = orders_df
                return RESULT_SUCCESS
            except Exception as e:
                return RESULT_ERROR + "_" + e.__str__()

        return RESULT_ERROR

    def on_tick_handler(self) -> str:
        order = OrderModel(command=OP_BUY, open_price=0, stop_loss=0.9, take_profit=1.1, lots=0.1, expiration_date=0, ticket=-1)
        self._orders_to_open = order.to_df()
        return self._orders_to_open.to_csv()#result

    def on_orders_changed_handler(self, orders_before: pd.DataFrame, orders_after: pd.DataFrame):
        return

    @staticmethod
    def order_to_str(type, open, sl, tp, lot, expiration_date, ticket = -1):
        return f'command:{type},open_price:{open},stop_loss:{sl},take_profit:{tp},lots:{lot},expiration_date:{expiration_date},ticket:{ticket}'


if __name__ == '__main__':
    bot = MtPyBotBase()
    pipe.pipe_server(bot.process_json_data)