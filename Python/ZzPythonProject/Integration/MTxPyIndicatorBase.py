import pandas as pd
import math


class MTxPyIndicatorBase:
    """Contains default basis for indicator"""
    def __init__(self, sym_tf_pairs: [], series_names: [], empty_value=math.nan):
        self.symbol_tf_pairs = sym_tf_pairs
        self.series_names = series_names
        self.empty_value = empty_value
        self.calculated_data = pd.DataFrame()
        self.last_calculated: tuple = None

    def calculate(self, df: pd.DataFrame, symbol: str, timeframe: int) -> pd.DataFrame:
        """df is supposed to be a Rates DF with (Symbol, Timeframe, Timestamp) multiindex."""

        if self._check_symbol_tf_needs_calc(symbol, timeframe):
            #possible shit with performance
            df_ix = df.loc[(symbol,timeframe,):(symbol,timeframe,)].index
            #df_ix = df[(df.index.get_level_values("symbol") == symbol) & (df.index.get_level_values("timeframe") == timeframe)].index
            ix_diff = df_ix.difference(self.calculated_data.index)
            diff_padding = pd.DataFrame(self.empty_value, columns=self.series_names, index=ix_diff)
            self.calculated_data = self.calculated_data.append(diff_padding)
            if not self.last_calculated:
                self.last_calculated = diff_padding.index.values[0]
            df_updates = df.loc[self.last_calculated:(symbol,timeframe,)]
            self.calculated_data = self._calculate_internal(df_updates)

        return self.calculated_data

    def _calculate_internal(self, df: pd.DataFrame) -> pd.DataFrame: #DF and
        """Override this to process data updates and return last calculated value"""
        raise NotImplementedError()

    def _check_symbol_tf_needs_calc(self, symbol, timeframe):
        for sym, tf in self.symbol_tf_pairs:
            if sym == symbol and tf == timeframe:
                return True
        return False
