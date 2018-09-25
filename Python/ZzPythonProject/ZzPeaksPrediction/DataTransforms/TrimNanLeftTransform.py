import numpy as np
import pandas as pd
from DataTransforms.LeftShiftedTransformBase import LeftShiftedTransformBase, LeftShiftedTransformParams


class TrimNanLeftTransformParams(LeftShiftedTransformParams):
    """Only periods=1 is currently supported."""
    nans_count: int #represents quantity of NaNs in the left side of the sequenceXY


#TODO TESTS!!!
class TrimNanLeftTransform(LeftShiftedTransformBase):
    params: TrimNanLeftTransformParams()

    def transform(self, series):
        self.params.last_input_series = series
        self.params.nans_count = self.get_first_not_nan_pos( series )
        nanless_series = series.loc[self.params.nans_count:]#pd.Series(series.loc[self.params.nans_count:].values)
        return nanless_series

    def inv_transform(self, series):
        nans_to_restore = self.params.last_input_series.loc[0:self.params.nans_count-1]
        res_series = pd.concat([nans_to_restore , pd.Series(series)], ignore_index=True)
        return res_series