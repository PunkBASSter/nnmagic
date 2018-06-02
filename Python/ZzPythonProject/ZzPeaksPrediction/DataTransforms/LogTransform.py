from DataTransforms.TransformBase import TransformBase
import math
import numpy as np
import pandas as pd

class LogTransform(TransformBase):

    _log_base = None
    log_base_limit = 9999999

    def transform(self, series, log_base=None):
        inp_lst = series.tolist()
        self._log_base = self._calc_log_base(inp_lst) if log_base is None else log_base
        res_lst = self._calc_logs(inp_lst)
        return pd.Series(res_lst)

    def inv_transform(self, series, log_base=None):
        inp_lst = series.tolist()
        _log_base = self._log_base if log_base is None else log_base
        res_lst = self._calc_exps(inp_lst, _log_base)
        return pd.Series(res_lst)

    def _calc_log_base(self, lst):
        log_base = max(abs(min(lst)), max(lst))
        log_base = min(log_base, self.log_base_limit)
        return log_base

    def _calc_logs(self, lst):
        res = []
        for l in lst:
            sign = -1 if l < 0 else 1
            res.append(math.log(abs(l), self._log_base) * sign)
        return res

    def _calc_exps(self, lst, reverse_log_base):
        log_base = reverse_log_base
        res = []
        for l in lst:
            sign = -1 if l < 0 else 1
            res.append(math.pow(log_base, abs(l)) * sign)
        return res