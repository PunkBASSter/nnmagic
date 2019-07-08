import pandas as pd
import math
from SymbolPeriodTimeContainer import SymbolPeriodTimeContainer


class MTxPyIndicatorBase:
    """Contains default basis for indicator"""
    def __init__(self, data_source, symbol_periods: {}, series_names: [], empty_value=math.nan):
        self.data_source = data_source
        self.symbol_periods = symbol_periods
        self.series_names = series_names
        self.empty_value = empty_value
        self.calculated_data = SymbolPeriodTimeContainer()
        self.last_calculated = {}

    def initialize(self):
        source_data_container = self.data_source.get_source_container()
        for symbol in self.symbol_periods:
            self.last_calculated[symbol] = {}
            self.calculated_data[symbol] = {}
            for period in self.symbol_periods[symbol]:
                padding = self._get_padding_df(source_data_container[symbol][period].index)
                self.last_calculated[symbol][period] = padding.index.values[0]
                self.calculated_data[symbol][period] = padding
                self.calculated_data = self._calculate_internal(symbol, period, source_data_container[symbol][period])

    def calculate(self, symbol: str, period: int, timestamp: int) -> SymbolPeriodTimeContainer:
        """timestamp_df is supposed to be a Rates DF with (Symbol, Timeframe, Timestamp) multiindex."""

        if self._is_calculation_required(symbol, period, timestamp):
            calculated_df = self.calculated_data[symbol][period]
            timestamp_df = self.data_source.calculate(symbol, period, timestamp)
            ix_diff = timestamp_df.index.difference(calculated_df.index)
            diff_padding = self._get_padding_df(ix_diff)

            self.calculated_data.extend_data(symbol, period, diff_padding)

            df_updates = timestamp_df.loc[self.last_calculated[symbol][period]:]
            self.calculated_data = self._calculate_internal(symbol, period, df_updates)

        return self.calculated_data

    def _calculate_internal(self, symbol, period, df: pd.DataFrame) -> SymbolPeriodTimeContainer: #DF and
        """Override this to process data updates and return last calculated value"""
        raise NotImplementedError()

    def _is_calculation_required(self, symbol, period, timestamp) -> bool:
        return symbol in self.symbol_periods and period in self.symbol_periods[symbol] and\
               self.last_calculated[symbol][period].tail(1).index.values[0] <= timestamp

    def _get_padding_df(self, index: pd.Index) -> pd.DataFrame:
        return pd.DataFrame(self.empty_value, columns=self.series_names, index=index)

    def get_source_container(self) -> SymbolPeriodTimeContainer:
        return self.calculated_data
