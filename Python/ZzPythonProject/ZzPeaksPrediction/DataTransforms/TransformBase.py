import pandas as pd

class TransformBase:

    def __init__(self, **kwargs):
        #for key, value in kwargs.items():
        #    setattr(self, key, value)
        self.__dict__.update( kwargs )

    def transform(self, series: pd.Series) -> pd.Series:
        return series

    def inv_transform(self, series: pd.Series) -> pd.Series:
        return series

    def __repr__(self):
        # todo implement method
        return f"{type(self)}"
