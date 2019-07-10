import pandas as pd
from DataTransforms.TransformBase import TransformBase


class ChainedTransform(TransformBase):

    def __init__(self, *args):
        super().__init__()
        self._transformation_sequence = []
        for arg in args:
            self._transformation_sequence.append(arg)

    def transform(self, series: pd.Series) -> pd.Series:
        series = pd.Series(series.values)
        length = len(self._transformation_sequence)
        if length < 2: raise ValueError("Sequence must contain at least 2 elements.")

        res = self._transformation_sequence[0].transform(series)
        for i in range(1, length):
            res = self._transformation_sequence[i].transform(res)

        return res

    def inv_transform(self, series: pd.Series) -> pd.Series:
        length = len(self._transformation_sequence)
        if length < 2: raise ValueError("Sequence must contain at least 2 elements.")

        res = self._transformation_sequence[length-1].inv_transform(series)
        for i in range(length-2, -1, -1):
            res = self._transformation_sequence[i].inv_transform(res)

        return res