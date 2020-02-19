import MetaTrader5 as mt5


class TesterTrade:

    def __init__(self, magic):
        self.magic = magic

    def buy(self, symbol, volume, price=0, sl=0, tp=0, expiration=0) -> int:
        tick = mt5.symbol_info_tick(symbol)

        order_type = mt5.ORDER_TYPE_BUY
        action = mt5.TRADE_ACTION_DEAL
        if price > 0:
            if price > tick.ask:
                action = mt5.TRADE_ACTION_PENDING
                order_type = mt5.ORDER_TYPE_BUY_STOP
            if price < tick.ask:
                order_type = mt5.ORDER_TYPE_BUY_LIMIT
                action = mt5.TRADE_ACTION_PENDING

        request = {
            "action": action,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "deviation": 10,
            "sl": sl,
            "tp": tp,
            "expiration": expiration,
            "magic": self.magic
        }

        send_res = mt5.order_send(request)
        if send_res.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order Send Failed")
            print(send_res)

        return send_res.order

    def sell(self, symbol, volume, price=0, sl=0, tp=0, expiration=0) -> int:
        tick = mt5.symbol_info_tick(symbol)

        order_type = mt5.ORDER_TYPE_SELL
        action = mt5.TRADE_ACTION_DEAL
        if price > 0:
            if price < tick.bid:
                action = mt5.TRADE_ACTION_PENDING
                order_type = mt5.ORDER_TYPE_SELL_STOP
            if price > tick.bid:
                order_type = mt5.ORDER_TYPE_SELL_LIMIT
                action = mt5.TRADE_ACTION_PENDING

        request = {
            "action": action,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "deviation": 10,
            "sl": sl,
            "tp": tp,
            "expiration": expiration,
            "magic": self.magic
        }

        send_res = mt5.order_send(request)
        if send_res.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order Send Failed")
            print(send_res)

        return send_res.order