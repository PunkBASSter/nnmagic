from scipy.stats import morestats as stats
from DataTransforms.TransformBase import TransformBase, TransformParams
import numpy as np
import pandas as pd


class BoxCoxTransformParams(TransformParams):
    lmbda = None
    alpha = None


class BoxCoxTransform(TransformBase):
    params: BoxCoxTransformParams

    def transform(self, series: pd.Series):
        # self.params.alpha = 123
        # self.params.lmbda= 345

        # result = stats.boxcox(series.values, lmbda=self.params.lmbda, alpha=self.params.alpha)
        result = stats.boxcox(series.values, **self.params)
        # Unpacking result tuple directly from scipy.boxcox(...) causes weird errors in bulk execution of tests!
        res, self.params.lmbda, *_ = result
        return pd.Series(res)

    def inv_transform(self, series: pd.Series):
        return self._inv_boxcox(series, self.params.lmbda)

    def _inv_boxcox(self, y, lmbda):
        if lmbda == 0:
            return np.exp(y)
        else:
            return np.exp(np.log(lmbda * y + 1) / lmbda)
