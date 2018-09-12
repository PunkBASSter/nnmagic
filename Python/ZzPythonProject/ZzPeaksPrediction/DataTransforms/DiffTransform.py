import numpy as np
import pandas as pd
from DataTransforms.LeftShiftedTransformBase import LeftShiftedTransformBase, LeftShiftedTransformParams


class DiffTransformParams(LeftShiftedTransformParams):
    """Only periods=1 is currently supported."""
    periods = 1
    #first_origin_element = None
    #nan_replacement_value = None
    #last_result_series = None


class DiffTransform(LeftShiftedTransformBase):
    params : DiffTransformParams()

    def transform(self, series):
        self.params.last_input_series= series
        #self.params.first_origin_element = series.iloc[0:1].values[0]
        diff_series = series.diff(periods=self.params.periods)

        #nan_replacement = self.params.nan_replacement_value
        #if nan_replacement is None:
        #    nan_replacement = result.iloc[1:2].tolist()[0]
        #result.iloc[0:1] = nan_replacement

        #self.params.shift_from_left = self._calc_shift(series)

        #self.params.last_result_series = result
        #result = diff_series.iloc[1:]

        return diff_series

    def inv_transform(self, series):
        last_input_series = self.params.last_input_series

        first_value_pos = self.get_last_nan_pos(series)
        calc_values = []
        res_series = pd.Series(data=last_input_series.iloc[0:first_value_pos]) #init with first original element
        for i in range(first_value_pos, len(last_input_series)):
            prev_value = last_input_series.values[i-1] #assumed to be shorter by 1 element
            current_diff = series.values[i]
            calc_values.append(prev_value + current_diff)

        res_series = pd.concat([res_series , pd.Series(calc_values)], ignore_index=True)

        return res_series
