import pandas as pd
import math
from SymbolPeriodTimeContainer import SymbolPeriodTimeContainer


class MTxPyDataSourceBase:

    def __init__(self, data_source, inp_symbol_periods: {}, out_series_names:[], empty_value=math.nan):
        self.data_source = data_source
        self.symbol_periods = inp_symbol_periods
        self.series_names = out_series_names
        self.empty_value = empty_value

    def calculate(self, symbol: str, period: int, timestamp: int) -> SymbolPeriodTimeContainer:
        raise NotImplementedError()




def resolve_data_source():
    pass