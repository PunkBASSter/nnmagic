class Trade:
    #todo make fields properties or dick with them :)
    open = 0
    sl = 0
    tp = 0
    spread = 0.0005
    lot = 0.01

    def try_close(self, current_price):
        """Compares stop order values with current_price and returns trade's outcome: profit/loss/in progress."""
        raise NotImplementedError("Subclass must implement abstract method")

    def validation_fail_condition(self, open, sl, tp): #todo find out how to make it protected
        """Determines the conditions when validation is failed."""
        return False

    def validate_input(self, open, sl, tp):
        if self.validation_fail_condition(open, sl, tp):
            return False
        return True

    def assign_levels(self, open, sl, tp):
        if not self.validate_input(open, sl, tp):
            return NoTrade()

        self.open = open
        self.sl = sl
        self.tp = tp
        return self

    def change_tp(self, k):
        """Changes Take Profit size multiplied by k."""
        return self


class NoTrade(Trade):
    def try_close(self, current_price):
        return 0


class BuyTrade(Trade):
    def change_tp(self, k):
        self.tp = self.open + (self.tp - self.open)*k
        return self if self.tp > self.open else NoTrade()

    def try_close(self, current_price):
        if current_price >= self.tp:
            return self.tp - self.open - self.spread, NoTrade()
        if current_price <= self.sl:
            return self.sl - self.open - self.spread, NoTrade()
        return 0, self

    def validation_fail_condition(self, open, sl, tp):
        return not tp > open > sl > 0


class SellTrade(Trade):
    def change_tp(self, k):
        self.tp = self.open - (self.open - self.tp)*k
        return self if self.tp < self.open else NoTrade()

    def try_close(self, current_price):
        if current_price <= self.tp:
            return self.open - self.tp - self.spread, NoTrade()
        if current_price >= self.sl:
            return self.open - self.sl - self.spread, NoTrade()
        return 0, self

    def validation_fail_condition(self, open, sl, tp):
        return not sl > open > tp > 0


def opening_strategy(sequence, predicted):
    #simple basic strategy
    trade = BuyTrade() if sequence[0] < sequence[1] else SellTrade()
    open = sequence[1]
    stop = min(sequence[0], sequence[2]) if isinstance(trade, BuyTrade) else min(sequence[0], sequence[2])
    take = predicted
    trade = trade.assign_levels(open, stop, take)

    stopsize = abs(open-stop)
    takesize = abs(take-open)
    k1 = 1.6 #tp/sl threshold
    k2 = 0.75 #0.75 #additional pessimism for forecast :)

    if takesize/stopsize > k1:
        return trade.change_tp(k2)
    else:
        return NoTrade()

    #return trade


def emulate_trading_on_series(start, price_series, predicted_series):
    trades = [0]
    balance = [0]
    price_total = len(price_series)
    limit = min(price_total, len(predicted_series))-1
    current_trade = NoTrade()
    i = start

    while i < limit - 1:
        if isinstance(current_trade, NoTrade):
            balance.append(balance[len(balance)-1])
            current_trade = opening_strategy([price_series[i], price_series[i - 1], price_series[i - 2]], predicted_series[i + 1])
        else:
            outcome, current_trade = current_trade.try_close(price_series[i+1])
            trades.append(outcome)
            balance.append(balance[len(balance) - 1] + trades[len(trades) - 1])
        i = i + 1
    return balance, trades