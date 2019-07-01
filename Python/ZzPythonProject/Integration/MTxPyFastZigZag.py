from MTxPyIndicatorBase import *


class MTxPyFastZigZag(MTxPyIndicatorBase):
    depth: float

    def __init__(self, caller, symbol, timeframe, depth):
        """Requires depth size in pips"""
        super().__init__(caller, {symbol: [timeframe]}, series_names=["zigzag"])
        self.symbol = symbol
        self.period = timeframe
        self.direction = 1
        self.depth = depth
        self.last_swing_size = 0

    def _calculate_internal(self, symbol, period, upd_df: pd.DataFrame):
        """Requires DataFrame containing columns called 'high' and 'low',
         calculates Fast ZigZag with constant depth as price range."""
        zz = self.calculated_data[self.symbol][self.period][self.series_names[0]]
        high = upd_df.high
        low = upd_df.low
        last = self.last_calculated[self.symbol][self.period]
        if upd_df.__len__() > 20:
            zz.iloc[0] = (high.iloc[0]+low.iloc[0])/2
        for ix in upd_df.index.values:
            if self.direction > 0:
                if high[ix] >= zz[last]:
                    zz[last] = self.empty_value
                    zz[ix] = high[ix]
                    last = ix
                else:
                    if low[ix] < zz[last] - self.get_depth():
                        zz[ix] = low[ix]
                        self.direction = -1
                        self.last_swing_size = zz[last] - zz[ix]
                        last = ix
            else:
                if low[ix] <= zz[last]:
                    zz[last] = self.empty_value
                    zz[ix] = low[ix]
                    last = ix
                else:
                    if high[ix] > zz[last] + self.get_depth():
                        zz[ix] = high[ix]
                        self.direction = 1
                        self.last_swing_size = zz[ix] - zz[last]
                        last = ix
        self.last_calculated[self.symbol][self.period] = last
        self.calculated_data[self.symbol][self.period][self.series_names[0]] = zz
        return self.calculated_data

    def get_depth(self):
        return self.depth

    def get_last_values(self, number: int) -> []:
        tmp = self.calculated_data.get_last_values(self.symbol, self.period, 1000)
        return tmp[tmp[self.series_names[0]] > 0][self.series_names[0]].tail(number).to_list()