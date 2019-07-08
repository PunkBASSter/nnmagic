from MTxPyFastZigZag import *


class MTxPyDeltaZigZag(MTxPyFastZigZag):
    """Differs from FastZZ only in Depth calculation (dynamic vs const)"""
    def __init__(self, data_source, symbol, timeframe, depth):
        super().__init__(data_source, symbol, timeframe, depth)

    def get_depth(self):
        return self.last_swing_size * self.depth #/ 100