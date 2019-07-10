from Transforms.LeftShiftedTransformBase import *

#TODO TESTS!!!
class TrimNanLeftTransform(LeftShiftedTransformBase):

    def __init__(self):
        super().__init__()
        self.nans_count = 0 # represents quantity of NaNs in the left side of the sequenceXY

    def transform(self, series):
        self.last_input_series = series
        self.nans_count = self.get_first_not_nan_pos(series)
        nanless_series = series.loc[self.nans_count:]#pd.Series(series.loc[self.params.nans_count:].values)
        return nanless_series

    def inv_transform(self, series):
        nans_to_restore = self.last_input_series.loc[0:self.nans_count-1]
        res_series = pd.concat([nans_to_restore , pd.Series(series)], ignore_index=True)
        return res_series