from Integration.MTxPyBotBase import *
from MTxPyDeltaZigZag import *


class SingleOrderBot(MTxPyBotBase):
    zigzag: MTxPyDeltaZigZag

    def __init__(self, magic_number, zz_depth):

        self.zigzag = MTxPyDeltaZigZag(zz_depth)
        super().__init__(magic_number, [self.zigzag])

    def on_init_handler(self) -> str:
        return RESULT_SUCCESS

    def on_tick_handler(self) -> str:

        last_zz = self.zigzag.get_last_values(4)
        #if last_zz[1] < last_zz[2] > last_zz[3] and last_zz[1] < last_zz[3]:
        if last_zz[2] < last_zz[3]:
            if self._active_orders.__len__() == 0:
                order = OrderModel(command=OP_BUYSTOP, open_price=last_zz[3], stop_loss=last_zz[2],
                                   take_profit=1.1, lots=0.1,
                                   expiration_date=0, ticket=-1, symbol=self._symbol)
                tmp_order = order.to_df()
                return tmp_order.to_csv()

        #if last_zz[1] > last_zz[2] < last_zz[3] and last_zz[1] > last_zz[3]:
        if last_zz[2] > last_zz[3]:
            if self._active_orders.__len__() == 0:
                order = OrderModel(command=OP_SELLSTOP, open_price=last_zz[3], stop_loss=last_zz[2],
                                   take_profit=0.9, lots=0.1,
                                   expiration_date=0, ticket=-1, symbol=self._symbol)
                tmp_order = order.to_df()
                return tmp_order.to_csv()

        active_orders = self.get_market_orders()
        #if active_orders.__len__() > 0:
#
        #    order = OrderModel(command=OP_UPDATE,
        #                       ticket=self._active_orders.iloc[0].ticket,
        #                       stop_loss=self._active_orders.iloc[0].stop_loss + 0.001)
        #    df = order.to_df()
        #    csv = df.to_csv()
        #    return csv
#
        #if self._active_orders.__len__() == 0:
        #    order = OrderModel(command=OP_BUY, open_price=0, stop_loss=0.9, take_profit=1.1, lots=0.1, expiration_date=0
        #                       , ticket=-1, symbol=self.symbol)
        #    tmp_order = order.to_df()
        #    return tmp_order.to_csv()

        return RESULT_SUCCESS

    def place_or_update_order(self, order: OrderModel):
        if self._active_orders.__len__() == 0:
            return order

        if order.exists_in_df(self._active_orders):
            return None

        #TODO Synchronize Order DELETE - Re-CREATE / UPDATE!

    def on_orders_changed_handler(self, orders_before: pd.DataFrame, orders_after: pd.DataFrame):
        if self._active_orders.__len__() > 0:

            pass #!!!!!!!!!!!!!!!!!!!!!!


if __name__ == '__main__':
    bot = SingleOrderBot(123123, zz_depth=0.003)
    pipe.pipe_server(bot.process_json_data)
