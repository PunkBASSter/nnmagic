import pandas as pd
import math


class MTxPyIndicatorBase:
    """Contains default basis for single symbol-timeframe indicator"""
    source_df: pd.DataFrame

    def __init__(self,series_names: [], empty_value=math.nan):
        self.last_calculated = 0
        self.series_names = series_names
        self.empty_value = empty_value
        self.series_names = series_names
        self.calculated_data = pd.DataFrame(index=["symbol","timeframe","timestamp"],columns=series_names)

    def calculate(self, df: pd.DataFrame, symbol: str, timeframe: int, new_bar: bool) -> pd.DataFrame:
        """df is supposed to be a Rates DF with (Symbol, Timeframe, Timestamp) multiindex."""
        self.source_df = df

        df_ix = df[(df.index.get_level_values("symbol") == symbol)
                   & (df.index.get_level_values("timeframe") == timeframe)].index

        ix_diff = df_ix.difference(self.calculated_data.index)
        diff_padding = pd.DataFrame(self.empty_value, columns=self.series_names, index=ix_diff)
        self.calculated_data = self.calculated_data.append(diff_padding)

        df_updates = df.iloc[max(self.last_calculated, 0):]
        self.calculated_data = self._calculate_internal(df_updates)
        return self.calculated_data

    def _calculate_internal(self, df: pd.DataFrame) -> pd.DataFrame: #DF and
        """Override this to process data updates and return last calculated value"""
        raise NotImplementedError()
