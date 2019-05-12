from FastZigZag import *

class DeltaZigZag(FastZigZag):
    """Differs from FastZZ only in Depth calculation (dynamic vs const)"""
    def __init__(self, depth):
        super().__init__(depth)

    def get_depth(self):
        return self.last_swing_size * self.depth #/ 100