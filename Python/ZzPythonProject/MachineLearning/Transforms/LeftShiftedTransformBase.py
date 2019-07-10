import math
from DataTransforms.TransformBase import *


class LeftShiftedTransformBase(TransformBase):

    def get_first_not_nan_pos(self, series: pd.Series):
        self.last_input_series = series
        for i in range(0, len(series)):
            if not math.isnan(series[i]):
                return i
