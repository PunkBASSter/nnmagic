import math
from DataTransforms.TransformBase import *


class LeftShiftedTransformBase(TransformBase):
    last_input_series: pd.Series

    def get_first_not_nan_pos(self, series: pd.Series):
        for i in range(0, len(series)):
            if not math.isnan(series[i]):
                return i
