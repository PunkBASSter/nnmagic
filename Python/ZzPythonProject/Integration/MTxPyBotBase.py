import json
import pandas as pd
import Mt5PipeConnector.PipeServer as pipe
from SymbolPeriodTimeContainer import SymbolPeriodTimeContainer

FLOAT_CMP_PRECISION = 0.00001

BOT_STATE_INIT = "INIT"
BOT_STATE_INIT_COMPLETE = "INIT_COMPLETE"
BOT_STATE_TICK = "TICK"
BOT_STATE_ORDERS = "ORDERS"
BOT_STATE_ORDERS_HISTORY = "ORDERS_HISTORY"
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

TF_STR = {
    1: "PERIOD_M1",
    2: "PERIOD_M2",
    3: "PERIOD_M3",
    4: "PERIOD_M4",
    5: "PERIOD_M5",
    6: "PERIOD_M6",
    10: "PERIOD_M10",
    12: "PERIOD_M12",
    15: "PERIOD_M15",
    20: "PERIOD_M20",
    30: "PERIOD_M30",
    60: "PERIOD_H1",
    120: "PERIOD_H2",
    180: "PERIOD_H3",
    240: "PERIOD_H4",
    360: "PERIOD_H6",
    480: "PERIOD_H8",
    720: "PERIOD_H12",
    1440: "PERIOD_D1",
    10080: "PERIOD_W1",
    43200: "PERIOD_MN1"
}


class OrderModel:
    def __init__(self, **kwargs):
        self.command: int = -1
        self.open_price: float = -1.0
        self.stop_loss: float = 0.0
        self.take_profit: float = 0.0
        self.lots: float = 0.0
        self.expiration_date: int = 0
        self.ticket: int = -1
        self.symbol: str = None
        self.__dict__.update(kwargs)

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame([self.__dict__])
        return df

    def check_exists(self, orders: pd.DataFrame) -> bool:
        res = orders[(orders.symbol == self.symbol)
                     & (abs(orders.open_price - self.open_price) < FLOAT_CMP_PRECISION)
                     & (abs(orders.stop_loss - self.stop_loss) < FLOAT_CMP_PRECISION)
                     & (abs(orders.take_profit - self.take_profit) < FLOAT_CMP_PRECISION)
                     & (abs(orders.lots - self.lots) < FLOAT_CMP_PRECISION)
                     & (orders.expiration_date == self.expiration_date)
                     & (orders.command % 2 == self.command % 2) #ODD for BUY and EVEN for SELL
                     & (OP_BUY <= orders.command)
                     & (orders.command <= OP_SELLSTOP)]

        return res.__len__() > 0

    @property
    def direction(self) -> int:
        if OP_BUY <= self.command <= OP_SELLSTOP:
            return 1 if (self.command & 1) == 0 else -1
        return 0


class MTxPyBotBase:
    """Encapsulates basic API calls and structure of MT bot business logic."""
    _symbol: str
    _timeframe: int
    _rates: SymbolPeriodTimeContainer

    def __init__(self, magic_number: int, indicators=None, only_new_bars=False):
        self.magic_number = magic_number
        self._only_new_bars = only_new_bars
        self._rates = SymbolPeriodTimeContainer()
        self._state = BOT_STATE_INIT
        self._active_orders = pd.DataFrame(columns=list(OrderModel().__dict__.keys()))
        self.indicators = indicators if indicators else pd.DataFrame(index=["symbol","timeframe"])

    def process_json_data(self, data_updates: str) -> str:
        """Callback handling pipe updates as JSON string containing mandatory 'state' object and optional data."""
        json_dict = json.loads(data_updates)
        self._state = json_dict["state"]

        #try:
        if self._state == BOT_STATE_INIT:
            self._symbol = json_dict["symbol"]
            self._timeframe = json_dict["timeframe"]
            df = pd.DataFrame(json_dict["rates"])
            df.set_index("timestamp",inplace=True)
            self._rates.add_values_with_key_check(self._symbol, self._timeframe,df)
            return RESULT_SUCCESS

        if self._state == BOT_STATE_INIT_COMPLETE:
            result = self.on_init_complete_handler()
            self._init_indicators()
            return result

        if self._state == BOT_STATE_TICK:
            self._symbol = json_dict["symbol"]
            self._timeframe = json_dict["timeframe"]
            on_tick_result = pd.DataFrame(columns=list(OrderModel().__dict__.keys()))
            df = pd.DataFrame(json_dict["rates"])
            df.set_index("timestamp", inplace=True)
            new_bar_detected = self._rates.add_values_by_existing_key(self._symbol, self._timeframe, df) > 0

        #DBG ON TICK PERFORMANCE
            #if self._active_orders.__len__() == 0:
            #    on_tick_result.command = OrderModel(command=OP_BUYLIMIT,lots=0.1,open_price=0.001)
            #else:
            #    on_tick_result.command = OrderModel(command=OP_REMOVE,ticket=self._active_orders.iloc[0].ticket)
            #return on_tick_result.to_csv()
        #/DBG PERF

            if not self._only_new_bars or new_bar_detected:
                self._recalculate_indicators(self._symbol, self._timeframe)
                on_tick_result = on_tick_result.append(self.on_tick_handler(self._symbol, self._timeframe),
                                                       ignore_index=False)
            res = on_tick_result.to_csv()
            return res

        if self._state == BOT_STATE_ORDERS:
            orders_df = pd.DataFrame(json_dict["orders"], columns=list(OrderModel().__dict__.keys()))
            prev_orders = self._active_orders
            if not orders_df.equals(prev_orders):
                self.on_orders_changed_handler(prev_orders, orders_df)
            self._active_orders = orders_df
            return RESULT_SUCCESS

        #except Exception as e:
            #return f'{RESULT_ERROR}_{self._state} {e.__str__()}'

        return RESULT_ERROR

    def get_source_container(self):
        return self._rates

    def _init_indicators(self):
        for ind in self.indicators:
            ind.initialize()

    def _recalculate_indicators(self, symbol, timeframe):
        for ind in self.indicators:
            ind.calculate(symbol, timeframe)

    def on_init_complete_handler(self) -> str:
        """Implement initialization of dependencies"""
        return RESULT_SUCCESS

    def on_tick_handler(self, symbol: str, timeframe: int) -> pd.DataFrame:
        """Implement ON Tick processing (excluding indicator updates). Returns DataFrame with commands(orders)."""
        return self._active_orders#raise NotImplementedError("Abstract method 'on_tick_handler' must be implemented.")

    def on_orders_changed_handler(self, orders_before: pd.DataFrame, orders_after: pd.DataFrame):
        pass

    def get_market_orders(self) -> pd.DataFrame:
        return self._active_orders[(self._active_orders.command == OP_BUY) | (self._active_orders.command == OP_SELL)]

    def get_pending_orders(self) -> pd.DataFrame:
        return self._active_orders[(self._active_orders.command >= OP_BUYLIMIT)
                                   | (self._active_orders.command <= OP_SELLSTOP)]

    def order_exists(self, order: OrderModel) -> bool:
        return order.check_exists(self._active_orders)

    def get_lots(self):
        return 0.1

    def cmd_remove_orders(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates commands to remove orders from given DF.
        :param df: DF of Orders to be removed
        :return: DF of OP_REMOVE based commands with tickets
        """
        res = df[df.ticket > -1]
        res.command = res.apply(lambda row: OP_REMOVE, axis=1)
        return res


if __name__ == '__main__':
    bot = MTxPyBotBase(123123)
    pipe.pipe_server(bot.process_json_data)