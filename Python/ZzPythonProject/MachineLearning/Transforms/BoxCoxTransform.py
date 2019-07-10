from scipy.stats import morestats as stats
from Transforms.TransformBase import *
import numpy as np
import pandas as pd


class BoxCoxTransform(TransformBase):

    def __init__(self):
        super().__init__()
        self.lmbda = None
        self.alpha = None

    def transform(self, series: pd.Series):

        result = stats.boxcox(series.values, lmbda=self.lmbda, alpha=self.alpha)
        # Unpacking result tuple directly from scipy.boxcox(...) causes weird errors in bulk execution of tests!
        res, self.lmbda, *_ = result
        return pd.Series(res)

    def inv_transform(self, series: pd.Series):
        return self._inv_boxcox(series, self.lmbda)

    def _inv_boxcox(self, y, lmbda):
        if lmbda == 0:
            return np.exp(y)
        else:
            return np.exp(np.log(lmbda * y + 1) / lmbda)
