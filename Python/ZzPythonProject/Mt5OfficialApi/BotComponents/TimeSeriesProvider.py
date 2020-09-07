import pymt5adapter as mt5
import numpy as np


class TimeSeriesProvider:

    def __init__(self, symbol, tf):
        self.symbol = symbol,
        self.tf = tf

    def get_series(self, symbol, tf, ):
        return self

    def fetch_history_by_pos(self, sym, tf, start_pos=1, chunk_size=10000):
        pos = start_pos
        oldest_bar = mt5.copy_rates_from(sym, tf, 0, 1)[0]

        res_arr = mt5.copy_rates_from_pos(sym, tf, pos, chunk_size)
        last_time = res_arr[0]['time']
        res_copied = res_arr.__len__()
        pos += chunk_size
        results = res_arr
        while (last_time > oldest_bar['time']) and (res_copied == chunk_size):
            res_arr = mt5.copy_rates_from_pos(sym, tf, pos, chunk_size)
            last_time = res_arr[0]['time']
            res_copied = res_arr.__len__()
            pos += chunk_size
            results = np.append(res_arr, results)
        return results

    def fetch_updates_


