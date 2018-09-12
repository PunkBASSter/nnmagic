import pandas as pd
import numpy as np
from DataTransforms.TransformBase import TransformBase, TransformParams


class ValueShiftTransformParams(TransformParams):
    extra_offset = 1.0
    final_shift = 0


class ValueShiftTransform(TransformBase):
    params: ValueShiftTransformParams

    def transform(self, series: pd.Series):
        res = series.values + self._calc_shift(series)
        return pd.Series(res)

    def inv_transform(self, series: pd.Series):
        res = series.values - self.params.final_shift
        return pd.Series(res)

    def _calc_shift(self, series):
        min = np.nanmin(series.values)
        if min > 0:
            self.params.final_shift = 0.
            return 0.

        if self.params.final_shift > 0:
            return self.params.final_shift
        self.params.final_shift = np.abs(min) + self.params.extra_offset

        return self.params.final_shift
