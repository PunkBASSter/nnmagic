import pandas as pd
import pickle

class TransformBase:

    def __init__(self, **kwargs):
        #for key, value in kwargs.items():
        #    setattr(self, key, value)
        self.__dict__.update(kwargs)

    def transform(self, series: pd.Series) -> pd.Series:
        return series

    def inv_transform(self, series: pd.Series) -> pd.Series:
        return series

    def __repr__(self):
        # todo implement method
        return f"{type(self)}"

    def save_transform(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_transform(path):
        with open(path, 'rb') as f:
            return pickle.load(f)