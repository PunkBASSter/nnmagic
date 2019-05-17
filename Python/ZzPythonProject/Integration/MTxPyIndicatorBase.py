import pandas as pd
import math


class MTxPyIndicatorBase:
    source_df: pd.DataFrame

    def __init__(self,series_names: [], empty_value=math.nan):
        self.last_calculated = 0
        self.series_names = series_names
        self.empty_value = empty_value
        self.series_names = series_names
        self.calculated_data = pd.DataFrame(columns=["timestamp"] + series_names)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        self.source_df = df

        if df.__len__() > self.calculated_data.__len__():
            start_index = self.calculated_data.last_valid_index()+1 if self.calculated_data.last_valid_index() else 0
            self.calculated_data = self.calculated_data.append(df.loc[start_index:][["timestamp"]],ignore_index=False)

        df_updates = df.loc[max(self.last_calculated, 0):]
        #self.calculated_data = self.calculated_data.append(df_updates[["timestamp"]], ignore_index=False)
        #self.calculated_data = self.calculated_data[~self.calculated_data.timestamp.duplicated(keep='last')]

        self.calculated_data = self._calculate_internal(df_updates)
        return self.calculated_data

    def _calculate_internal(self, df: pd.DataFrame) -> pd.DataFrame: #DF and
        """Override this to process data updates and return last calculated value"""
        raise NotImplementedError()
