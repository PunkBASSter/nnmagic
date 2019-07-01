import pandas as pd
import math
from SymbolPeriodTimeContainer import SymbolPeriodTimeContainer


class MTxPyIndicatorBase:
    """Contains default basis for indicator"""
    def __init__(self, caller, symbol_periods: {}, series_names: [], empty_value=math.nan):
        self.caller = caller
        self.symbol_periods = symbol_periods
        self.series_names = series_names
        self.empty_value = empty_value
        self.calculated_data = SymbolPeriodTimeContainer()
        self.last_calculated = {}

    def initialize(self):
        source_data_container = self.caller.get_source_container()
        for symbol in self.symbol_periods:
            self.last_calculated[symbol] = {}
            self.calculated_data[symbol] = {}
            for period in self.symbol_periods[symbol]:
                padding = self._get_padding_df(source_data_container[symbol][period].index)
                self.last_calculated[symbol][period] = padding.index.values[0]
                self.calculated_data[symbol][period] = padding
                self.calculated_data = self._calculate_internal(symbol, period, source_data_container[symbol][period])

    def calculate(self, symbol: str, period: int) -> SymbolPeriodTimeContainer:
        """timestamp_df is supposed to be a Rates DF with (Symbol, Timeframe, Timestamp) multiindex."""

        if self._check_symbol_tf_needs_calc(symbol, period):
            calculated_df = self.calculated_data[symbol][period]
            timestamp_df = self.caller.get_source_container()[symbol][period]
            ix_diff = timestamp_df.index.difference(calculated_df.index)
            diff_padding = self._get_padding_df(ix_diff)

            self.calculated_data.extend_data(symbol, period, diff_padding)

            df_updates = timestamp_df.loc[self.last_calculated[symbol][period]:]
            self.calculated_data = self._calculate_internal(symbol, period, df_updates)

        return self.calculated_data

    def _calculate_internal(self, symbol, period, df: pd.DataFrame) -> SymbolPeriodTimeContainer: #DF and
        """Override this to process data updates and return last calculated value"""
        raise NotImplementedError()

    def _check_symbol_tf_needs_calc(self, symbol, period) -> bool:
        return symbol in self.symbol_periods and period in self.symbol_periods[symbol]

    def _get_padding_df(self, index: pd.Index) -> pd.DataFrame:
        return pd.DataFrame(self.empty_value, columns=self.series_names, index=index)
