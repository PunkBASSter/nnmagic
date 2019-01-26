from FastZigZag import *

class DeltaZigZag(FastZigZag):

    def __init__(self, depth):
        super().__init__( depth)

    #def calc_zz(self, df: pd.DataFrame):
        '''Requires DataFrame containing columns called 'high' and 'low',
         calculates Delta ZigZag based on depth * previous swing size.'''

    #    return super().calc_zz(df)

        #if self.prev_res is None:
        #    zz = pd.Series( 0. for _ in range( self.last_i, df.__len__() ) )
        #else:
        #    ext = [e for e in range( self.last_i + 1, df.__len__() )]
        #    zz = self.prev_res.append( pd.Series( 0, index=ext ), ignore_index=False )
#
        #last = self.prev_idx
        #for i in range( self.last_i, df.__len__()):
        #    if self.direction > 0:
        #        if df.high[i] > zz[last]:
        #            zz[last] = 0
        #            zz[i] = df.high[i]
        #            last = i
        #        else:
        #            if df.low[i] < zz[last] - self.get_depth():
        #                zz[i] = df.low[i]
        #                self.direction = -1
        #                self.last_swing_size = zz[last] - zz[i]
        #                last = i
        #    else:
        #        if df.low[i] < zz[last]:
        #            zz[last] = 0
        #            zz[i] = df.low[i]
        #            last = i
        #        else:
        #            if df.high[i] > zz[last] + self.get_depth():
        #                zz[i] = df.high[i]
        #                self.direction = 1
        #                self.last_swing_size = zz[i] - zz[last]
        #                last = i
#
        #self.prev_idx = last
        #self.last_i = df.__len__() - 1
        #self.prev_res = zz
        #return zz

    def get_depth(self):
        return self.last_swing_size * self.depth / 100