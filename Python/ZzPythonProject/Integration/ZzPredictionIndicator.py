import pandas as pd
from Integration.MTxPyIndicatorBase import MTxPyIndicatorBase
import TransformBase


class ZzPredictionIndicator(MTxPyIndicatorBase):

    def __init__(self, data_source, symbol_periods: {}, transform_path, model_path):
        super().__init__(data_source, symbol_periods, "ZigzagPredictions")
        self.transform = TransformBase.load_transform(transform_path)

    def _calculate_internal(self, symbol, period, df: pd.DataFrame):

        return self._data_container

    def check_training_required(self) -> bool:
        return False

    def _train(self):
        #OVERRIDE
        self.transform.save_transform(self.data_file_name)
        pass
