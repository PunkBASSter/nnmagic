from MTxPyIndicatorBase import *


class MTxPyFastZigZag(MTxPyIndicatorBase):
    depth: float

    def __init__(self, depth):
        """Requires depth size in pips"""
        super().__init__(series_names=["zigzag"])
        self.direction = 1
        self.depth = depth
        self.last_swing_size = 0

    def _calculate_internal(self, df: pd.DataFrame):
        """Requires DataFrame containing columns called 'high' and 'low',
         calculates Fast ZigZag with constant depth as price range."""
        zz = self.calculated_data[self.series_names[0]]
        last = self.last_calculated
        if last <= 0:
            zz[0] = df.close[0]
        for i in range(last, self.calculated_data.__len__()):
            if self.direction > 0:
                if df.high[i] > zz[last]:
                    zz[last] = self.empty_value
                    zz[i] = df.high[i]
                    last = i
                else:
                    if df.low[i] < zz[last] - self.get_depth():
                        zz[i] = df.low[i]
                        self.direction = -1
                        self.last_swing_size = zz[last] - zz[i]
                        last = i
            else:
                if df.low[i] < zz[last]:
                    zz[last] = self.empty_value
                    zz[i] = df.low[i]
                    last = i
                else:
                    if df.high[i] > zz[last] + self.get_depth():
                        zz[i] = df.high[i]
                        self.direction = 1
                        self.last_swing_size = zz[i] - zz[last]
                        last = i
        self.last_calculated = last
        self.calculated_data[self.series_names[0]] = zz
        return self.calculated_data

    def get_depth(self):
        return self.depth

    def get_last_values(self, number: int) -> []:
        tmp = self.calculated_data.tail(1000)
        return tmp[tmp[self.series_names[0]] > 0][self.series_names[0]].tail(number).to_list()