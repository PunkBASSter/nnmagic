import MetaTrader5 as mt5
from RealTimeEndpoint import RealTimeEndpoint


class BotBase:

    def __init__(self, endpoint, data_storage, indicators):
        self.endpoint = endpoint
        self.data_storage = data_storage
        self.indicators = indicators

    def initialize(self):
        self.endpoint.initialize()

    def process(self):
        pass

    def on_tick(self, tick):
        pass

    def on_new_bar(self, timestamp):
        pass