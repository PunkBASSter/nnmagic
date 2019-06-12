from Integration.MTxPyBotBase import *
from MTxPyDeltaZigZag import *


class SingleOrderBot(MTxPyBotBase):
    zigzag: MTxPyDeltaZigZag

    def __init__(self, symbol, timeframe, magic_number, zz_depth, remove_opposite_orders):

        self.zigzag = MTxPyDeltaZigZag(symbol, timeframe, zz_depth)
        super().__init__(magic_number, [self.zigzag])
        self.remove_opposite_orders = remove_opposite_orders

    def on_tick_handler(self, symbol: str, timeframe: int) -> pd.DataFrame:
        orders = self._active_orders
        orders = orders[orders.symbol == symbol]
        buy_positions = orders[orders.command == OP_BUY]
        sell_positions = orders[orders.command == OP_SELL]
        buy_orders = orders[orders.command == OP_BUYSTOP]# | orders.command == OP_BUYLIMIT]
        sell_orders = orders[orders.command == OP_SELLSTOP]# | orders.command == OP_SELLLIMIT]
        result = pd.DataFrame()#TODO add columns? - HZ

        if buy_positions.__len__() > 0 or sell_positions.__len__() > 0:
            return result

        if buy_positions.__len__() == 0:
            order = self.buy_condition()
            if order:
                order.lots = self.get_lots()
                order.symbol = symbol

                if order.check_exists(orders):
                    result = result.append(OrderModel(command=OP_NONE).to_df().to_csv(), ignore_index=False)

                if buy_orders.__len__() == 0:
                    result = result.append(order.to_df(), ignore_index=False)
                else:
                    ticket = buy_orders.first().ticket
                    order.command = OP_UPDATE
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
                    result = result.append(OrderModel(command=OP_NONE).to_df().to_csv(), ignore_index=False)

                if sell_orders.__len__() == 0:
                    result = result.append(order.to_df(), ignore_index=False)
                else:
                    ticket = sell_orders.first().ticket
                    order.command = OP_UPDATE
                    order.ticket = ticket
                    result = result.append(order.to_df(), ignore_index=False)

                if self.remove_opposite_orders:
                    result = result.append(self.cmd_remove_orders(buy_orders), ignore_index=False)

        return result

    def buy_condition(self):
        last_zz = self.zigzag.get_last_values(4)
        if last_zz[2] < last_zz[3]:
            tp = last_zz[3] + (last_zz[3] - last_zz[2])
            return OrderModel(command=OP_BUYSTOP, open_price=last_zz[3], stop_loss=last_zz[2], take_profit=tp,
                              expiration_date=0)
        return None

    def sell_condition(self):
        last_zz = self.zigzag.get_last_values(4)
        if last_zz[2] > last_zz[3]:
            tp = last_zz[3] - (last_zz[2]-last_zz[3])
            return OrderModel(command=OP_SELLSTOP, open_price=last_zz[3], stop_loss=last_zz[2], take_profit=tp,
                              expiration_date=0)
        return None

    def on_orders_changed_handler(self, orders_before: pd.DataFrame, orders_after: pd.DataFrame):
        pass


if __name__ == '__main__':
    bot = SingleOrderBot("EURUSD", 60, 123123, zz_depth=0.003, remove_opposite_orders=True)
    pipe.pipe_server(bot.process_json_data)
