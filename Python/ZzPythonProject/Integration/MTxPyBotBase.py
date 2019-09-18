import json
import pandas as pd
import Mt5PipeConnector.PipeServer as pipe
from MTxPyDataSource import MTxPyDataSource

FLOAT_CMP_PRECISION = 0.00001

BOT_STATE_INIT = "INIT"
BOT_STATE_INIT_TRAINING = "INIT_TRAINING"
BOT_STATE_INIT_OFFLINE = "INIT_OFFLINE"
BOT_STATE_INIT_COMPLETE = "INIT_COMPLETE"
BOT_STATE_SAVE_DATA = "SAVE_DATA"
BOT_STATE_TICK = "TICK"
BOT_STATE_ORDERS = "ORDERS"
BOT_STATE_ORDERS_HISTORY = "ORDERS_HISTORY"
RESULT_SUCCESS = "OK"
RESULT_ERROR = "ERROR"
RESULT_EXIT = "EXIT"

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
                     & (orders.command % 2 == self.command % 2)  # ODD for BUY and EVEN for SELL
                     & (OP_BUY <= orders.command)
                     & (orders.command <= OP_SELLSTOP)]

        return res.__len__() > 0

    @property
    def direction(self) -> int:
        if OP_BUY <= self.command <= OP_SELLSTOP:
            return 1 if (self.command & 1) == 0 else -1
        return 0


class MTxPyBotBase(MTxPyDataSource):
    """Encapsulates basic API calls and structure of MT bot business logic."""

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: str):
        self._state = state

    def __init__(self, magic_number: int, only_new_bars=True):
        super().__init__()
        self._symbol = None
        self._timeframe = None
        self.magic_number = magic_number
        self._only_new_bars = only_new_bars
        self._state = ""
        self._active_orders = pd.DataFrame(columns=list(OrderModel().__dict__.keys()))
        self.is_offline = False

    def process_json_data(self, data_updates: str) -> str:
        """Callback handling pipe updates as JSON string containing mandatory 'state' object and optional data."""
        json_dict = json.loads(data_updates)
        self.state = json_dict["state"]

        if self.state == BOT_STATE_INIT:
            self._symbol = json_dict["symbol"]
            self._timeframe = json_dict["timeframe"]
            df = pd.DataFrame(json_dict["rates"])
            df.set_index("timestamp", inplace=True)
            self._data_container.add_values_with_key_check(self._symbol, self._timeframe, df)
            MTxPyDataSource._global_rates_container = self._data_container
            return RESULT_SUCCESS

        if self.state == BOT_STATE_INIT_TRAINING:
            MTxPyDataSource._global_rates_container = self._data_container
            result = self.initialize()
            self._init_indicators()
            # self.save_data()
            self.is_offline = True
            self.train()
            # TODO RESET ITERATORS TO RE-INITIALIZE IN LIVE MODE?
            # exit(0)
            return result

        if self.state == BOT_STATE_SAVE_DATA:
            self.save_data()
            return RESULT_SUCCESS

        if self.state == BOT_STATE_INIT_OFFLINE:
            self.is_offline = True
            return RESULT_SUCCESS

        if self.state == BOT_STATE_INIT_COMPLETE:
            if self.is_offline:
                self.load_data()
            MTxPyDataSource._global_rates_container = self._data_container
            result = self.initialize()
            self._init_indicators()
            return result

        if self.state == BOT_STATE_TICK:
            self._symbol = json_dict["symbol"]
            self._timeframe = json_dict["timeframe"]
            on_tick_result = pd.DataFrame(columns=list(OrderModel().__dict__.keys()))
            df = pd.DataFrame(json_dict["rates"])
            df.set_index("timestamp", inplace=True)
            new_bar_detected = self.is_offline or \
                               self._data_container.add_values_by_existing_key(self._symbol, self._timeframe, df) > 0
            MTxPyDataSource._global_rates_container = self._data_container

            last_timestamp = df.tail(1).index.values[0]

            # DBG
            if last_timestamp == 1488236400:
                print("LAST_TS_2017_02_27__2300")

            if not self._only_new_bars or new_bar_detected:
                self._recalculate_indicators(self._symbol, self._timeframe, last_timestamp)
                on_tick_result = on_tick_result.append(self.on_tick(self._symbol, self._timeframe),
                                                       ignore_index=False, sort=False)
            res = on_tick_result.to_csv()
            return res

        if self.state == BOT_STATE_ORDERS:
            orders_df = pd.DataFrame(json_dict["orders"], columns=list(OrderModel().__dict__.keys()))
            prev_orders = self._active_orders
            if not orders_df.equals(prev_orders):
                self.on_orders_changed(prev_orders, orders_df)
            self._active_orders = orders_df
            return RESULT_SUCCESS

        return RESULT_ERROR

    def _init_indicators(self):
        for ind in self._data_sources.values():
            ind.initialize(self.is_offline)

    def _recalculate_indicators(self, symbol, timeframe, timestamp):
        for ind in self._data_sources.values():
            ind.calculate(symbol, timeframe, timestamp)

    def initialize(self) -> str:
        """Implement initialization of dependencies"""
        return RESULT_SUCCESS

    def on_tick(self, symbol: str, timeframe: int) -> pd.DataFrame:
        """Implement ON Tick processing (excluding indicator updates). Returns DataFrame with commands(orders)."""
        return self._active_orders  # raise NotImplementedError("Abstract method 'on_tick' must be implemented.")

    def on_orders_changed(self, orders_before: pd.DataFrame, orders_after: pd.DataFrame):
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
