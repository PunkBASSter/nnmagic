from Integration.MTxPyBotBase import *


class IntegrationTestBot(MTxPyBotBase):

    def on_tick_handler(self) -> str:

        #if self._active_orders.__len__() > 0:
        #    order = OrderModel(command=OP_REMOVE, ticket=self._active_orders.iloc[0].ticket)
        #    df = order.to_df()
        #    csv = df.to_csv()
        #    return csv

        if self._active_orders.__len__() > 0:
            order = OrderModel(command=OP_UPDATE, ticket=self._active_orders.iloc[0].ticket, stop_loss=self._active_orders.iloc[0].stop_loss + 0.001)
            df = order.to_df()
            csv = df.to_csv()
            return csv

        if self._active_orders.__len__() == 0:
            order = OrderModel(command=OP_BUY, open_price=0, stop_loss=0.9, take_profit=1.1, lots=0.1, expiration_date=0, ticket=-1)
            self._orders_to_open = order.to_df()
            return self._orders_to_open.to_csv()


if __name__ == '__main__':
    bot = IntegrationTestBot()
    pipe.pipe_server(bot.process_json_data)
