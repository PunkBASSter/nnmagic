from DataTransforms.TransformBase import TransformBase, TransformParams
import math
import pandas as pd


class LogTransformParams(TransformParams):
    log_base = None
    log_base_limit = 9999999
    inv_log_base_multiplier = 1


class LogTransform(TransformBase):
    params : LogTransformParams

    def transform(self, series: pd.Series):

        inp_lst = series.tolist()

        if not self.params.log_base:
            self.params.log_base = self._calc_log_base(inp_lst)

        res_lst = self._calc_logs(inp_lst)

        return pd.Series(res_lst)

    def inv_transform(self, series: pd.Series):
        inp_lst = series.tolist()
        _log_base = self.params.log_base * self.params.inv_log_base_multiplier
        res_lst = self._calc_exps(inp_lst, _log_base)
        return pd.Series(res_lst)

    def _calc_log_base(self, lst):
        log_base = max(abs(min(lst)), max(lst))
        log_base = min(log_base, self.params.log_base_limit)
        return log_base

    def _calc_logs(self, lst):
        res = []
        for l in lst:
            sign = -1 if l < 0 else 1
            res.append(math.log(abs(l), self.params.log_base) * sign)
        return res

    def _calc_exps(self, lst, reverse_log_base):
        log_base = reverse_log_base
        res = []
        for l in lst:
            sign = -1 if l < 0 else 1
            res.append(math.pow(log_base, abs(l)) * sign)
        return res
