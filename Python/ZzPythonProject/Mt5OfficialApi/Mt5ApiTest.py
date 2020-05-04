import MetaTrader5 as mt5
import time
from BotComponents.Trade import Trade
from ZzPythonProject.Integration.SymbolPeriodTimeContainer import SymbolPeriodTimeContainer
import numpy as np
import pandas as pd

mt5.initialize()

symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_H1
tick = mt5.symbol_info_tick(symbol)

terminal_info = mt5.terminal_info()
#rates_range = mt5.copy_rates_range(symbol, timeframe, 1572230396, 1582238396)


def get_bar_seconds(tf):
    if tf < mt5.TIMEFRAME_H1:
        return tf*60
    if mt5.TIMEFRAME_H1 <= tf < mt5.TIMEFRAME_W1:
        return (tf - 0x4000)*60*60
    if tf == mt5.TIMEFRAME_W1:
        return (tf - 0x8000)*5*24*60*60
    if tf == mt5.TIMEFRAME_MN1:
        return (tf - 0xC000)*22*24*60*60
    return 0

ololo = mt5.copy_rates_range(symbol, timeframe, 1531278000, tick.time)
ololo2 = mt5.copy_rates_range(symbol, timeframe, 1530918000, 1531278000-1)


#Below method is WORKING!!
def fetch_history_by_pos(sym, tf, start_pos = 1, chunk_size=10000):
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


res = fetch_history_by_pos(symbol, timeframe)
res_df = pd.DataFrame(res)

def fetch_history(sym, tf):
    last_tick = mt5.symbol_info_tick(sym)
    oldest_bar = mt5.copy_rates_from(sym, tf, 0, 1)[0]
    copy_start_time = last_tick.time
    copy_start_time = 1531278000
    chunk_size = 10000

    res_arr = mt5.copy_rates_from(sym, tf, copy_start_time, chunk_size)
    copy_start_time = res_arr[0]['time']
    results = res_arr
    while copy_start_time > oldest_bar['time']:
        arr = mt5.copy_rates_from(sym, tf, copy_start_time, chunk_size)
        copy_start_time = arr[0]['time'] - 10 #exclude overlapping
        results = np.append(arr, results)
    return results

res = fetch_history(symbol, timeframe)

bars = mt5.copy_rates_from(symbol, timeframe, 0, 1)
bar_time_capacity = get_bar_seconds(timeframe)
chunk_size = 100

time_window = chunk_size*bar_time_capacity
current_start_time = bars[0]['time']
current_end_time = current_start_time + time_window
while current_end_time < tick.time:
    res = mt5.copy_rates_range(symbol, timeframe, current_start_time, current_end_time)
    current_start_time = current_end_time + bar_time_capacity
    current_end_time = current_start_time + time_window
    np.append(bars, res)





rates_from = mt5.copy_rates_from(symbol, timeframe, tick.time, terminal_info.maxbars)
rates_from_pos = mt5.copy_rates_from_pos(symbol, timeframe, 0, 100)
rates_range = mt5.copy_rates_range(symbol, timeframe, 1582230396, 1582238396)
rates_range1 = mt5.copy_rates_range(symbol, timeframe, 0, tick.time)
container = SymbolPeriodTimeContainer()

tr = Trade(123)

success = tr.buy(symbol, 0.01, p.ask+0.002, p.ask-0.002, p.ask+0.004)

while True:
    p = mt5.symbol_info_tick(symbol)
    print(p.bid, '/', p.ask)

    if p.ask > prev_price and buy_price == 0:
        print("Buy ", p.ask)
        r = mt5.Buy(symbol, 0.01)
        if r.retcode == mt5.TRADE_RETCODE_DONE:
            buy_price = p.ask
    elif buy_price > 0 and p.ask + dev < buy_price:
        print("Buy(close) ", p.bid)
        mt5.Close(symbol)
        buy_price = 0

    prev_price = p.ask
    time.sleep(1)

mt5.shutdown()




#initialize(path=None)                              Establish connection with the MetaTrader 5 Terminal
#wait()                                             Wait for the MetaTrader 5 Terminal to connect to a broker's server
#shutdown()                                         Disconnect from the MetaTrader 5 Terminal
#
#version()                                          Get the MetaTrader 5 Terminal version
#terminal_info()                                    Get the parameters of the MetaTrader 5 terminal
#account_info()                                     Returns information of current account
#
#copy_ticks_from(symbol, from, count, flags)                Get ticks starting from the specific date
#copy_ticks_range(symbol, from, to, flags)                  Get ticks from the specified period
#copy_rates_from(symbol, timeframe, from, count)            Get bars starting from the specific date
#copy_rates_from_pos(symbol, timeframe, start_pos, count)   Get bars starting from the specified position
#copy_rates_range(symbol, timeframe, date_from, date_to)    Get bars from the specified period
#
#positions_total()                                          Returns the number of open positions
#positions_get([symbol=\"SYMBOL\"],[ticket=TICKET])         Returns all open positions, can be filtered by symbol or ticket
#
#orders_total()                                             Returns the number of orders
#orders_get([symbol=\"SYMBOL\"],[ticket=TICKET])            Returns all orders, can be filtered by symbol or ticket
#
#history_orders_total(from, to)                             Returns the number of orders in selected range from the history
#history_orders_get(from, to)                               Returns orders in selected range from the history or filtered by position id, ticket
#
#history_deals_total(from, to)                              Returns the number of deals in selected range from the history
#history_deals_get(from, to)                                Returns deals in selected range from the history or filtered by position id, ticket
#
#order_check(request)                                                Checks if there are enough funds to execute the required trade operation
#order_send(request)                                                 Sends trade requests to a server
#order_calc_margin(action, symbol, volume, price)                    Calculates the margin required for the specified order
#order_calc_profit(action, symbol, volume, price_open, price_close)  Calculates the profit for the current account, in the current market conditions, based on the parameters passed
#
#symbol_info(symbol)                                        Returns full information for a specified symbol
#symbol_info_tick(symbol)                                   Returns current prices of a specified symbol
#symbol_select(symbol,[enable])                             Selects a symbol in the Market Watch window or removes a symbol from the window