import pandas as pd
import numpy as np
from DataTransforms.TransformBase import TransformBase, TransformParams


class ShiftToPositiveTransformParams(TransformParams):
    extra_offset = 1.1
    final_shift = 0


class ShiftToPositiveTransform(TransformBase):

    def __init__(self, params :ShiftToPositiveTransformParams):
        self.transform_params = params

    def transform(self, series: pd.Series):
        shift = self._calc_shift(series)
        res = series.values + shift
        return pd.Series(res)

    def inv_transform(self, series: pd.Series):
        res = series.values - self.transform_params.final_shift
        return pd.Series(res)

    def _calc_shift(self, series):
        min = series.min()
        if min > 0:
            self.transform_params.final_shift = 0.
            return 0.

        if self.transform_params.final_shift > 0:
            return self.transform_params.final_shift
        self.transform_params.final_shift = np.abs(min) + self.transform_params.extra_offset

        return self.transform_params.final_shift