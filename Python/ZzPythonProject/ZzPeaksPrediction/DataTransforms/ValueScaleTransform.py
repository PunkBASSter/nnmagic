import pandas as pd
import numpy as np
from DataTransforms.TransformBase import TransformBase, TransformParams


class ValueScaleTransformParams( TransformParams ):
    target_abs_level = 10
    multiplier = 1


class ValueScaleTransform( TransformBase ):

    def __init__(self, params :ValueScaleTransformParams):
        self.transform_params = params

    def transform(self, series: pd.Series):
        res = series.values * self._calc_multiplier(series.values)
        return pd.Series(res)

    def inv_transform(self, series: pd.Series):
        res = series.values / self.transform_params.multiplier
        return pd.Series(res)

    def _calc_multiplier(self, values):
        if not self.transform_params.multiplier == 1:
            return self.transform_params.multiplier

        max_abs = max( abs( values.min() ), values.max() )
        self.transform_params.multiplier = self.transform_params.target_abs_level / max_abs
        return self.transform_params.multiplier