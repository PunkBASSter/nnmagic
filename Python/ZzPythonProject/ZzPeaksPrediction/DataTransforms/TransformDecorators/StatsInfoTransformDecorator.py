from DataTransforms.TransformBase import TransformBase, TransformParams
import HelperFunctions.StatisticsHelperFunctions as shf
import pandas as pd

class StatsInfoTransformDecorator(TransformBase):

    _decorated_object = None

    def __init__(self, decorated_object :TransformBase):
        self._decorated_object = decorated_object

    def transform(self, series: pd.Series):
        result = self._decorated_object.transform(series)

        print(type(self._decorated_object))
        self._decorated_object.transform_params.tostring()
        print("\n")
        shf.is_normal(result)
        shf.is_stationary(result)
        print("-------------------\n")

        return result