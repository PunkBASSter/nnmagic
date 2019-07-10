import pandas as pd
from Integration.MTxPyIndicatorBase import MTxPyIndicatorBase
import ChainedTransform


#import ChainedTransform


class ZzPredictionIndicator(MTxPyIndicatorBase):

    def __init__(self, data_source, symbol_periods: {}, transform_path, model_path):
        super().__init__(data_source, symbol_periods, "ZigzagPredictions")
        self.transform = ChainedTransform.load_transform(transform_path)

    def _calculate_internal(self, symbol, period, df: pd.DataFrame):

        return self.calculated_data
