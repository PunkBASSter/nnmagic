import MetaTrader5 as mt5
import time
from BotComponents.Trade import Trade
from SymbolPeriodTimeContainer import SymbolPeriodTimeContainer
import numpy as np
import pandas as pd


def get_bar_seconds(tf):
    if tf < mt5.TIMEFRAME_H1:
        return tf * 60
    if mt5.TIMEFRAME_H1 <= tf < mt5.TIMEFRAME_W1:
        return (tf - 0x4000) * 60 * 60
    if tf == mt5.TIMEFRAME_W1:
        return (tf - 0x8000) * 5 * 24 * 60 * 60
    if tf == mt5.TIMEFRAME_MON1:
        return (tf - 0xC000) * 22 * 24 * 60 * 60
    return 0


def fetch_history_by_pos(sym, tf, start_pos=1, chunk_size=10000):
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