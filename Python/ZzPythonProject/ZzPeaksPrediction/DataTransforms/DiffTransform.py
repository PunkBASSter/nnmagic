import numpy as np
from DataTransforms.TransformBase import TransformBase

class DiffTransform(TransformBase):
    """Only periods=1 is currently supported."""
    _periods = 1
    _first_origin = None

    def transform(self, series, periods=1):
        self._first_origin = series.iloc[0:1]
        self._periods = periods
        return series.diff(periods=periods)

    def inv_transform(self, diffs, first_origin_element=None):
        if not first_origin_element == None:
            self._first_origin = first_origin_element
        return self._inv_diff(self._first_origin, diffs)

    def _inv_diff(self, src_first, diff):
        diff.iloc[0:1] = src_first
        res = diff.cumsum()
        return res

