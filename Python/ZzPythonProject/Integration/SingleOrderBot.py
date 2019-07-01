import Integration.MTxPyBotBase as bb
import pandas as pd
from Integration.MTxPyBotBase import OrderModel
from Integration.MTxPyBotBase import MTxPyBotBase
from MTxPyDeltaZigZag import MTxPyDeltaZigZag
import Mt5PipeConnector.PipeServer as pipe

class SingleOrderBot(MTxPyBotBase):

    def __init__(self, symbol, timeframe, magic_number, zz_depth, remove_opposite_orders):

        self.symbol = symbol
        self.timeframe = timeframe
        self.zz_depth = zz_depth
        self.zigzag = None
        super().__init__(magic_number, [self.zigzag])
        self.remove_opposite_orders = remove_opposite_orders

    def on_init_complete_handler(self):
        self.zigzag = MTxPyDeltaZigZag(self, self.symbol, self.timeframe, self.zz_depth)
        self.indicators = [self.zigzag]
        return bb.RESULT_SUCCESS

    def on_tick_handler(self, symbol: str, timeframe: int) -> pd.DataFrame:
        orders = self._active_orders
        orders = orders[orders.symbol == symbol]
        buy_positions = orders[orders.command == bb.OP_BUY]
        sell_positions = orders[orders.command == bb.OP_SELL]
        buy_orders = orders[orders.command == bb.OP_BUYSTOP]# | orders.command == OP_BUYLIMIT]
        sell_orders = orders[orders.command == bb.OP_SELLSTOP]# | orders.command == OP_SELLLIMIT]
        result = pd.DataFrame()#TODO add columns? - HZ

#        if buy_positions.__len__() > 0 or sell_positions.__len__() > 0:
#            return result

        if buy_positions.__len__() == 0:
            order = self.buy_condition()
            if order:
                order.lots = self.get_lots()
                order.symbol = symbol

                if order.check_exists(orders):
                    result = result.append(OrderModel(command=bb.OP_NONE).to_df(), ignore_index=False)

                if buy_orders.__len__() == 0:
                    result = result.append(order.to_df(), ignore_index=False)
                else:
                    ticket = buy_orders.iloc[0].ticket
                    order.command = bb.OP_UPDATE
                    order.ticket = ticket
                    result = result.append(order.to_df(), ignore_index=False)

                if self.remove_opposite_orders:
                    result = result.append(self.cmd_remove_orders(sell_orders), ignore_index=False)

        if sell_positions.__len__() == 0:
            order = self.sell_condition()
            if order:
                order.lots = self.get_lots()
                order.symbol = symbol

                if order.check_exists(orders):
                    result = result.append(OrderModel(command=bb.OP_NONE).to_df(), ignore_index=False)

                if sell_orders.__len__() == 0:
                    result = result.append(order.to_df(), ignore_index=False)
                else:
                    ticket = sell_orders.iloc[0].ticket
                    order.command = bb.OP_UPDATE
                    order.ticket = ticket
                    result = result.append(order.to_df(), ignore_index=False)

                if self.remove_opposite_orders:
                    result = result.append(self.cmd_remove_orders(buy_orders), ignore_index=False)

        return result

    def buy_condition(self):
        last_zz = self.zigzag.get_last_values(4)
        if last_zz[1] < last_zz[0]:
            tp = last_zz[0] + (last_zz[0] - last_zz[1])
            return OrderModel(command=bb.OP_BUYSTOP, open_price=last_zz[0], stop_loss=last_zz[1], take_profit=tp,
                              expiration_date=0)
        return None

    def sell_condition(self):
        last_zz = self.zigzag.get_last_values(4)
        if last_zz[1] > last_zz[0]:
            tp = last_zz[0] - (last_zz[1]-last_zz[0])
            return OrderModel(command=bb.OP_SELLSTOP, open_price=last_zz[0], stop_loss=last_zz[1], take_profit=tp,
                              expiration_date=0)
        return None

    def on_orders_changed_handler(self, orders_before: pd.DataFrame, orders_after: pd.DataFrame):
        pass


if __name__ == '__main__':
    bot = SingleOrderBot("EURUSD", 60, 123123, zz_depth=0.5, remove_opposite_orders=False)
    pipe.pipe_server(bot.process_json_data)
