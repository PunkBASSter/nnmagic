from DataTransforms.TransformBase import *
import math
import pandas as pd
import numpy as np


class LogTransform(TransformBase):

    log_base : float
    log_base_limit : float
    inv_log_base_multiplier : float

    def __init__(self, **kwargs):
        self.log_base = None
        self.log_base_limit = 9999999
        self.inv_log_base_multiplier = 1
        super().__init__(**kwargs)

    def transform(self, series: pd.Series):

        if not self.log_base:
            self.log_base = self._calc_log_base(series)

        transformed = series.transform(lambda x: math.log(x, self.log_base))
        return pd.Series(transformed)

    def inv_transform(self, series: pd.Series):
        log_base = self.log_base * self.inv_log_base_multiplier

        res = series.transform(lambda x: log_base ** x)
        return res

    def _calc_log_base(self, series: pd.Series):
        log_base = max(abs(np.nanmin(series)), np.nanmax(series))
        log_base = min(log_base, self.log_base_limit)
        return log_base
