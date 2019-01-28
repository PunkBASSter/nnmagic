from DataTransforms.LeftShiftedTransformBase import *


class DiffTransform(LeftShiftedTransformBase):

    def transform(self, series):
        self.last_input_series = series
        nan_pos = self.get_first_not_nan_pos( series )
        diff_series = series.iloc[nan_pos:].diff()
        return diff_series

    def inv_transform(self, series):
        last_input_series = self.last_input_series

        first_value_pos = self.get_first_not_nan_pos( series )
        calc_values = []
        res_series = pd.Series(data=last_input_series.iloc[0:first_value_pos]) #init with first original element
        for i in range(first_value_pos, len(series)):
            calc_values.append(last_input_series.values[i-1] + series.values[i])

        res_series = pd.concat([res_series , pd.Series(calc_values)], ignore_index=True)
        return res_series