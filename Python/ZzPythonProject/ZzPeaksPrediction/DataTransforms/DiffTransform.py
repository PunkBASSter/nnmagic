import numpy as np
import pandas as pd
from DataTransforms.TransformBase import TransformBase, TransformParams


class DiffTransformParams(TransformParams):
    """Only periods=1 is currently supported."""
    periods = 1
    first_origin_element = None
    nan_replacement_value = None
    last_result_series = None
    last_input_series = None
    shift_from_left = 0


class DiffTransform(TransformBase):
    params = DiffTransformParams()

    def transform(self, series):
        self.params.last_input_series= series
        self.params.first_origin_element = series.iloc[0:1].values[0]
        result = series.diff(periods=self.params.periods)

        nan_replacement = self.params.nan_replacement_value
        if nan_replacement is None:
            nan_replacement = result.iloc[1:2].tolist()[0]
        result.iloc[0:1] = nan_replacement

        self.params.shift_from_left = 1 #TODO Create generic algorithm

        self.params.last_result_series = result
        return result

    def inv_transform(self, series, last_input_series = params.last_input_series):
        if not last_input_series:
            last_input_series = self.params.last_input_series

        calc_values = []
        res_series = pd.Series(data=last_input_series.iloc[0:self.params.shift_from_left])
        for i in range(self.params.shift_from_left,len(series)):
            prev_value = last_input_series.values[i-1]
            current_diff = series.values[i]
            calc_values.append(prev_value + current_diff)

        res_series = pd.concat([res_series , pd.Series(calc_values)], ignore_index=True)

        return res_series
