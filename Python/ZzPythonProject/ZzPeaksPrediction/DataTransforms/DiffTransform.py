import numpy as np
import pandas as pd
from DataTransforms.TransformBase import TransformBase, TransformParams


class DiffTransformParams(TransformParams):
    """Only periods=1 is currently supported."""
    periods = 1
    first_origin_element = None
    nan_replacement_value = None


class DiffTransform(TransformBase):
    params = DiffTransformParams()

    def transform(self, series):
        self.params.first_origin_element = series.iloc[0:1].values[0]
        result = series.diff(periods=self.params.periods)

        nan_replacement = self.params.nan_replacement_value
        if nan_replacement is None:
            nan_replacement = result.iloc[1:2].tolist()[0]
        result.iloc[0:1] = nan_replacement

        return result

    def inv_transform(self, series):
        return self._inv_diff(self.params.first_origin_element, series)

    def _inv_diff(self, src_first, diff):
        diff.iloc[0:1] = src_first
        res = diff.cumsum()
        return res
