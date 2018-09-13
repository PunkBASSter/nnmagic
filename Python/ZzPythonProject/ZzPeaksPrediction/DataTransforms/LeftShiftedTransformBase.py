import numpy as np
import pandas as pd
import math
from DataTransforms.TransformBase import TransformBase, TransformParams

class LeftShiftedTransformParams(TransformParams):
    """Only periods=1 is currently supported."""
    last_input_series: pd.Series

class LeftShiftedTransformBase(TransformBase):
    params : LeftShiftedTransformParams

    def get_last_nan_pos(self, series : pd.Series):
        for i in range(0, len(series)):
            if not math.isnan(series[i]):
                return i