import json
import pandas as pd
import Mt5PipeConnector.PipeServer as pipe

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
                     & OP_BUY <= orders.command
                     & orders.command <= OP_SELLSTOP]

        return res.__len__() > 0

    @property
    def direction(self) -> int:
        if OP_BUY <= self.command <= OP_SELLSTOP:
            return 1 if self.command % 2 == 0 else -1
        return 0


class MTxPyBotBase:
    """Encapsulates basic API calls and structure of MT bot business logic."""

    def __init__(self, magic_number: int, indicators=None):
        self.magic_number = magic_number
        self._rates = {}
        self._state = BOT_STATE_INIT
        self._active_orders = pd.DataFrame(columns=list(OrderModel.__dict__.keys()))
        self.indicators = indicators if indicators else []
        self._symbol = None

    def process_json_data(self, data_updates: str) -> str:
        """Callback handling pipe updates as JSON string containing mandatory 'state' object and optional data."""
        json_dict = json.loads(data_updates)
        self._state = json_dict["state"]

        #try:
        if self._state == BOT_STATE_INIT:
            self._symbol = json_dict["symbol"]
            self._update_rates_data(self._symbol, json_dict["rates"])
            return RESULT_SUCCESS

        if self._state == BOT_STATE_INIT_COMPLETE:
            self._symbol = json_dict["symbol"]
            result = self.on_init_handler()
            self._recalculate_indicators(self._symbol)
            return result

        if self._state == BOT_STATE_TICK:
            self._symbol = json_dict["symbol"]
            rates =  json_dict["rates"]
            self._update_rates_data(self._symbol, rates)
            on_tick_result = pd.DataFrame(columns=list(OrderModel().__dict__.keys()))
            on_tick_result.append(self.on_tick_handler(), ignore_index=False)
            return on_tick_result.to_csv()

        if self._state == BOT_STATE_ORDERS:
            orders_df = pd.DataFrame(json_dict["orders"])
            prev_orders = self._active_orders
            if not orders_df.equals(prev_orders):
                self.on_orders_changed_handler(prev_orders, orders_df)
            self._active_orders = orders_df
            return RESULT_SUCCESS

        #except Exception as e:
            #return f'{RESULT_ERROR}_{self._state} {e.__str__()}'

        return RESULT_ERROR

    def _update_rates_data(self, symbol: str, rates_upd: []) -> None:
        updates_df = pd.DataFrame(rates_upd)
        if not self._rates.__contains__(symbol):
            self._rates[symbol] = updates_df
            return

        cur_rates = self._rates[symbol]
        if cur_rates["timestamp"].loc[cur_rates.last_valid_index()] ==\
                updates_df["timestamp"].loc[updates_df.first_valid_index()]:
            self._rates[symbol].loc[cur_rates.last_valid_index()] = updates_df.loc[updates_df.first_valid_index()]
            self._recalculate_indicators(symbol)
            return

        self._rates[symbol] = cur_rates.append(updates_df, ignore_index=True)
        #self._rates[symbol] = cur_rates[~cur_rates.timestamp.duplicated(keep='last')]

    def _recalculate_indicators(self, symbol):
        for ind in self.indicators:
            ind.calculate(self._rates[symbol])

    def on_init_handler(self) -> str:
        """Implement initialization of dependencies"""
        raise NotImplementedError("Abstract method 'on_init_handler' must be implemented.")

    def on_tick_handler(self) -> pd.DataFrame:
        """Implement ON Tick processing (excluding indicator updates). Returns DataFrame with commands(orders)."""
        raise NotImplementedError("Abstract method 'on_tick_handler' must be implemented.")

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