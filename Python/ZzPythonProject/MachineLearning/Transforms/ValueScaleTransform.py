import numpy as np
from Transforms.TransformBase import *


class ValueScaleTransform(TransformBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_abs_level = 1
        self.multiplier = 1

    def transform(self, series: pd.Series):
        res = series.values * self._calc_multiplier(series.values)
        return pd.Series(res)

    def inv_transform(self, series: pd.Series):
        res = series.values / self.multiplier
        return pd.Series(res)

    def _calc_multiplier(self, values):
        if not self.multiplier == 1:
            return self.multiplier

        max_abs = max(abs(np.nanmin(values)), abs(np.nanmax(values)))
        self.multiplier = self.target_abs_level / max_abs
        return self.multiplier
