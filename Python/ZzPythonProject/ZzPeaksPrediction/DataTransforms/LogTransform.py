from DataTransforms.TransformBase import TransformBase, TransformParams
import math
import pandas as pd
import numpy as np


class LogTransformParams(TransformParams):
    log_base = None
    log_base_limit = 9999999
    inv_log_base_multiplier = 1


class LogTransform(TransformBase):
    params: LogTransformParams

    def transform(self, series: pd.Series):

        if not self.params.log_base:
            self.params.log_base = self._calc_log_base(series)

        transformed = series.transform(lambda x: math.log(x, self.params.log_base))
        return pd.Series(transformed)

    def inv_transform(self, series: pd.Series):
        #inp_lst = series.tolist()
        log_base = self.params.log_base * self.params.inv_log_base_multiplier

        res = series.transform(lambda x: log_base ** x)
        return res

    def _calc_log_base(self, series: pd.Series):
        log_base = max(abs(np.nanmin(series)), np.nanmax(series))
        log_base = min(log_base, self.params.log_base_limit)
        #print(f"Calculated log base: {log_base}")
        return log_base
