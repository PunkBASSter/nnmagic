import pandas as pd

class TransformParams:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr( self, key, value )

class TransformBase:

    transform_params = TransformParams()

    def transform(self, series: pd.Series):
        raise NotImplementedError("Subclass must implement abstract method")

    def inv_transform(self, series: pd.Series):
        raise NotImplementedError("Subclass must implement abstract method")

