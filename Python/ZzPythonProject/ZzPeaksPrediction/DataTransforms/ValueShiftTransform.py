import numpy as np
from DataTransforms.TransformBase import *


class ValueShiftTransform(TransformBase):
    extra_offset : float
    final_shift : float

    def __init__(self, **kwargs):
        self.extra_offset = 1.0
        self.final_shift = 0
        super().__init__(**kwargs)

    def transform(self, series: pd.Series):
        res = series.values + self._calc_shift(series)
        return pd.Series(res)

    def inv_transform(self, series: pd.Series):
        res = series.values - self.final_shift
        return pd.Series(res)

    def _calc_shift(self, series):
        minval = np.nanmin(series.values)
        if minval > 0:
            self.final_shift = 0.
            return 0.

        if self.final_shift > 0:
            return self.final_shift
        self.final_shift = np.abs(minval) + self.extra_offset

        return self.final_shift
