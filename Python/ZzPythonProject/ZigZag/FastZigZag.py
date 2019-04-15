import pandas as pd

class FastZigZag:
    prev_idx : int
    direction: int
    depth : float
    last_i : int
    prev_res : pd.Series
    last_swing_size: int

    def __init__(self, depth):
        '''Requires depth size in pips'''
        self.prev_idx = 0
        self.direction = 1
        self.depth = depth
        self.last_i = 0
        self.prev_res = None
        self.last_swing_size = 0

    def calc_zz(self, df: pd.DataFrame):
        '''Requires DataFrame containing columns called 'high' and 'low',
         calculates Fast ZigZag with constant depth as price range.'''

        if self.prev_res is None:
            zz = pd.Series( 0. for _ in range( self.last_i, df.__len__() ) )
        else:
            ext = [e for e in range( self.last_i + 1, df.__len__())]
            zz = self.prev_res.append( pd.Series(0, index=ext), ignore_index=False)

        last = self.prev_idx
        for i in range( self.last_i, df.__len__() ):
            if self.direction > 0:
                if df.high[i] > zz[last]:
                    zz[last] = 0
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
                    zz[last] = 0
                    zz[i] = df.low[i]
                    last = i
                else:
                    if df.high[i] > zz[last] + self.get_depth():
                        zz[i] = df.high[i]
                        self.direction = 1
                        self.last_swing_size = zz[i] - zz[last]
                        last = i

        self.prev_idx = last
        self.last_i = df.__len__() - 1
        self.prev_res = zz
        return zz

    def get_depth(self):
        return self.depth
