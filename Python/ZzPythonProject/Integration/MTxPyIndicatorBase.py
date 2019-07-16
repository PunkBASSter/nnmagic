import pandas as pd
import math
import copy
from SymbolPeriodTimeContainer import SymbolPeriodTimeContainer


class MTxPyIndicatorBase:
    """Contains default basis for indicator"""
    def __init__(self, data_source, symbol_periods: {}, series_names: [], empty_value=math.nan, offline=False):
        self.data_source = data_source
        self.symbol_periods = symbol_periods
        self.series_names = series_names
        self.empty_value = empty_value
        self.calculated_data = SymbolPeriodTimeContainer()
        self.last_calculated = {}
        self.is_offline = offline
        self.calculate = self._calc_offline if offline else self._calc_live
        self.calculated_data_offline = None #stores the all data in offline mode, actual at the moment is moved to self.calculated_data

    def initialize(self, offline = False):
        source_data_container = self.data_source.get_source_container()
        for symbol in self.symbol_periods:
            self.last_calculated[symbol] = {}
            self.calculated_data[symbol] = {}
            for period in self.symbol_periods[symbol]:
                padding = self._get_padding_df(source_data_container[symbol][period].index)
                self.last_calculated[symbol][period] = padding.index.values[0]
                self.calculated_data[symbol][period] = padding
                self.calculated_data = self._calculate_internal(symbol, period, source_data_container[symbol][period])

        self.is_offline = offline
        if self.is_offline:
            self.calculate = self._calc_offline if offline else self._calc_live
            self.calculated_data_offline = copy.deepcopy(self.calculated_data)

    def _calc_live(self, symbol: str, period: int, timestamp: int) -> SymbolPeriodTimeContainer:
        if self._is_calculation_required(symbol, period, timestamp):
            calculated_df = self.calculated_data[symbol][period]
            timestamp_df = self.data_source.calculate(symbol, period, timestamp)
            ix_diff = timestamp_df.index.difference(calculated_df.index)
            diff_padding = self._get_padding_df(ix_diff)

            self.calculated_data.extend_data(symbol, period, diff_padding)

            df_updates = timestamp_df.loc[self.last_calculated[symbol][period]:]
            self.calculated_data = self._calculate_internal(symbol, period, df_updates)

        return self.calculated_data

    def _calc_offline(self, symbol: str, period: int, timestamp: int) -> SymbolPeriodTimeContainer:
        self.last_calculated[symbol][period] = timestamp
        tmp = self.calculated_data[symbol][period]
        self.calculated_data_offline[symbol][period] = tmp[tmp.index <= timestamp]
        return self.calculated_data_offline

    def _calculate_internal(self, symbol, period, df: pd.DataFrame) -> SymbolPeriodTimeContainer: #DF and
        """Override this to process data updates and return last calculated value"""
        raise NotImplementedError()

    def _is_calculation_required(self, symbol, period, timestamp) -> bool:
        return symbol in self.symbol_periods and period in self.symbol_periods[symbol] and\
               self.last_calculated[symbol][period] <= timestamp

    def _get_padding_df(self, index: pd.Index) -> pd.DataFrame:
        return pd.DataFrame(self.empty_value, columns=self.series_names, index=index)

    def get_source_container(self) -> SymbolPeriodTimeContainer:
        return self.calculated_data

    def export_to_csv(self, file_path, file_name_pattern):
        for item in self.symbol_periods.items():
            current_df = self.calculated_data_offline[item[0]][item[1]]
            fname = f"{file_path}\\{file_name_pattern}_{item[0]}_{item[1]}.csv"
            current_df.to_csv(fname)

    def initialize_from_csv(self, sym_tf_path):
        self.is_offline = True
        pass