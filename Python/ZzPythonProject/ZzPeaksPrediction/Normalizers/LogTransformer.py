import math


class LogTransformer:

    _log_base = None
    _log_base_limit = 9999999
    _reverse_log_base_multiplier = 1

    def _calc_log_base(self, lst):
        self._log_base = max(abs(min(lst)), max(lst))
        self._log_base = min(self._log_base, self._log_base_limit)
        return self._log_base

    def calc_logs(self, lst):
        self._calc_log_base(lst)
        res = []
        for l in lst:
            sign = -1 if l < 0 else 1
            res.append(math.log(abs(l), self._log_base) * sign)
        return res

    def calc_exps(self, lst):
        log_base = self._log_base * self._reverse_log_base_multiplier
        res = []
        for l in lst:
            sign = -1 if l < 0 else 1
            res.append(math.pow(log_base, abs(l)) * sign)
        return res