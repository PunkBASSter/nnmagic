import MetaTrader5 as mt5
from RealTimeEndpoint import RealTimeEndpoint
import Utils


class BotBase:
    _symbol_periods: {}

    def __init__(self, symbol_periods :{}, indicators: []):
        self.indicators = indicators
        self._symbol_periods = symbol_periods

    def initialize(self):
        if not mt5.initialize():
            print("initialize() failed")
            mt5.shutdown()
        history = Utils.fetch_history_by_pos()

    def deinitialize(self):
        mt5.shutdown()

    def process(self):
        pass

    def on_tick(self, tick):
        pass

    def on_new_bar(self, bar):
        pass