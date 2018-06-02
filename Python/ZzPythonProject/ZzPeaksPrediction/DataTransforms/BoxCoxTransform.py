from scipy import stats
from DataTransforms.TransformBase import TransformBase
import numpy as np

class BoxCoxTransform(TransformBase):

    _lambda = None
    _alpha = None

    def transform(self, series, lmbda=None, alpha=None):
        self._alpha = alpha
        res, self._lambda = stats.boxcox(series, lmbda=lmbda, alpha=alpha)
        return res

    def inv_transform(self, series, lmbda=None):
        if lmbda is None:
            return self._inv_boxcox(series, self._lambda)
        return self._inv_boxcox(series, lmbda)

    def _inv_boxcox(self, y, lmbda):
        if lmbda == 0:
            return (np.exp(y))
        return (np.exp(np.log(lmbda * y + 1) / lmbda))
