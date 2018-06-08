import pandas as pd

class TransformParams:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr( self, key, value )

    def tostring(self):
        #todo implement method
        return ""

class TransformBase:

    transform_params = None

    def transform(self, series: pd.Series):
        return series

    def inv_transform(self, series: pd.Series):
        return series

