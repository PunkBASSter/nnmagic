import numpy as np
from Transforms.LeftShiftedTransformBase import *


class DivisionTransform(LeftShiftedTransformBase):

    def transform(self, series):
        self.last_input_series = series

        first_value_pos = self.get_first_not_nan_pos( series )
        calc_values = []
        res_series = pd.Series(data=series.iloc[0:first_value_pos])
        res_series = pd.concat([res_series, pd.Series(np.NaN)])
        for i in range(first_value_pos+1, len(series)):
            calc_values.append(series.values[i] / series.values[i-1])

        res_series = pd.concat([res_series, pd.Series(calc_values)], ignore_index=True)
        return res_series

    def inv_transform(self, series):
        last_input_series = self.last_input_series

        first_value_pos = self.get_first_not_nan_pos( series )
        calc_values = []
        res_series = pd.Series(data=last_input_series.iloc[0:first_value_pos])
        for i in range(first_value_pos, len(series)):
            calc_values.append(last_input_series.values[i-1] * series.values[i])

        res_series = pd.concat([res_series, pd.Series(calc_values)], ignore_index=True)

        return res_series
