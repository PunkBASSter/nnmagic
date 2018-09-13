import pandas as pd
import numpy as np
from DataTransforms.TransformBase import TransformBase, TransformParams


class ValueScaleTransformParams(TransformParams):
    target_abs_level = 1
    multiplier = 1


class ValueScaleTransform(TransformBase):
    params: ValueScaleTransformParams

    def transform(self, series: pd.Series):
        res = series.values * self._calc_multiplier(series.values)
        return pd.Series(res)

    def inv_transform(self, series: pd.Series):
        res = series.values / self.params.multiplier
        return pd.Series(res)

    def _calc_multiplier(self, values):
        if not self.params.multiplier == 1:
            return self.params.multiplier

        max_abs = max(abs(np.nanmin(values)), abs(np.nanmax(values)))
        self.params.multiplier = self.params.target_abs_level / max_abs
        return self.params.multiplier
