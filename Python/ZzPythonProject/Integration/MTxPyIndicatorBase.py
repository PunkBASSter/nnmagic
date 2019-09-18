import pandas as pd
import copy
from SymbolPeriodTimeContainer import SymbolPeriodTimeContainer
from MTxPyDataSource import MTxPyDataSource


class MTxPyIndicatorBase(MTxPyDataSource):
    """Contains default basis for indicator"""
    def __init__(self, data_sources: {}, symbol_periods: {}, series_names: []):
        super().__init__()
        self._data_sources = data_sources
        self.symbol_periods = symbol_periods
        self.series_names = series_names
        self.calculate = self._calc_live
        self.calculated_data_offline = None #stores the all data in offline mode, actual at the moment is moved to self._data_container

    def initialize(self, offline=False):
        self.is_offline = offline
        self._init_last_processed()
        if offline:
            self.calculate = self._calc_offline
            self.load_data()
            self.calculated_data_offline = copy.deepcopy(self._data_container)
            return

        for data_source in self._data_sources.values():
            data_source.initialize(offline)
        for symbol in self.symbol_periods:
            self._data_container[symbol] = {}
            for period in self.symbol_periods[symbol]:
                last_timestamp = MTxPyDataSource._global_rates_container.get_last_timestamp(symbol, period)
                padding = self._get_padding_df(symbol, period)
                self._data_container[symbol][period] = padding
                self._data_container = self._calculate_internal(symbol, period, last_timestamp)

    def _calc_live(self, symbol: str, period: int, timestamp: int) -> SymbolPeriodTimeContainer:
        if self._is_calculation_required(symbol, period, timestamp):
            for data_source in self._data_sources.values():
                data_source.calculate(symbol, period, timestamp)

            diff_padding = self._get_padding_df(symbol, period)
            self._data_container.extend_data(symbol, period, diff_padding)
            self._data_container = self._calculate_internal(symbol, period, timestamp)

        return self._data_container

    def _calc_offline(self, symbol: str, period: int, timestamp: int) -> SymbolPeriodTimeContainer:
        if self._is_calculation_required(symbol, period, timestamp):
            self.last_processed[symbol][period] = timestamp
            tmp = self.calculated_data_offline[symbol][period]
            self._data_container[symbol][period] = tmp[tmp.index <= timestamp]
        return self._data_container

    def _calculate_internal(self, symbol, period, timestamp) -> SymbolPeriodTimeContainer: #DF and
        """Override this to process data updates and return last calculated value"""
        raise NotImplementedError()

    #todo replace with sym-tf-event registration
    def _is_calculation_required(self, symbol, period, timestamp) -> bool:
        return symbol in self.symbol_periods and period in self.symbol_periods[symbol] and\
               self.last_processed[symbol][period] <= timestamp

    def _get_padding_df(self, symbol, period) -> pd.DataFrame:
        idx = MTxPyDataSource._global_rates_container[symbol][period].loc[self.last_processed[symbol][period]:].index
        return pd.DataFrame(self.empty_value, columns=self.series_names, index=idx)

    def train_model(self):
        pass

    def _init_last_processed(self):
        for symbol in self.symbol_periods:
            self.last_processed[symbol] = {}
            for period in self.symbol_periods[symbol]:
                first_timestamp = MTxPyDataSource._global_rates_container.get_first_timestamp(symbol, period)
                self.last_processed[symbol][period] = first_timestamp