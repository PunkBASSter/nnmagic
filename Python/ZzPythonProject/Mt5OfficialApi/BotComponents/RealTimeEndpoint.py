import MetaTrader5 as mt5
from Integration.SymbolPeriodTimeContainer import SymbolPeriodTimeContainer

class RealTimeEndpoint:

    def __init__(self):
        self.data_storage = SymbolPeriodTimeContainer()

    def initialize(self):
        mt5.initialize()


    def fetch_bars(self):
        pass

    def fetch_ticks(self):
        pass

    # initialize(path=None)                              Establish connection with the MetaTrader 5 Terminal
    # wait()                                             Wait for the MetaTrader 5 Terminal to connect to a broker's server
    # shutdown()                                         Disconnect from the MetaTrader 5 Terminal
    #
    # version()                                          Get the MetaTrader 5 Terminal version
    # terminal_info()                                    Get the parameters of the MetaTrader 5 terminal
    # account_info()                                     Returns information of current account
    #
    # copy_ticks_from(symbol, from, count, flags)                Get ticks starting from the specific date
    # copy_ticks_range(symbol, from, to, flags)                  Get ticks from the specified period
    # copy_rates_from(symbol, timeframe, from, count)            Get bars starting from the specific date
    # copy_rates_from_pos(symbol, timeframe, start_pos, count)   Get bars starting from the specified position
    # copy_rates_range(symbol, timeframe, date_from, date_to)    Get bars from the specified period
    #
    # positions_total()                                          Returns the number of open positions
    # positions_get([symbol=\"SYMBOL\"],[ticket=TICKET])         Returns all open positions, can be filtered by symbol or ticket
    #
    # orders_total()                                             Returns the number of orders
    # orders_get([symbol=\"SYMBOL\"],[ticket=TICKET])            Returns all orders, can be filtered by symbol or ticket
    #
    # history_orders_total(from, to)                             Returns the number of orders in selected range from the history
    # history_orders_get(from, to)                               Returns orders in selected range from the history or filtered by position id, ticket
    #
    # history_deals_total(from, to)                              Returns the number of deals in selected range from the history
    # history_deals_get(from, to)                                Returns deals in selected range from the history or filtered by position id, ticket
    #
    # order_check(request)                                                Checks if there are enough funds to execute the required trade operation
    # order_send(request)                                                 Sends trade requests to a server
    # order_calc_margin(action, symbol, volume, price)                    Calculates the margin required for the specified order
    # order_calc_profit(action, symbol, volume, price_open, price_close)  Calculates the profit for the current account, in the current market conditions, based on the parameters passed
    #
    # symbol_info(symbol)                                        Returns full information for a specified symbol
    # symbol_info_tick(symbol)                                   Returns current prices of a specified symbol
    # symbol_select(symbol,[enable])