from scipy.stats import morestats as stats
from DataTransforms.TransformBase import TransformBase, TransformParams
import numpy as np
import pandas as pd

class BoxCoxTransformParams(TransformParams):
    lmbda = None
    alpha = None


class BoxCoxTransform(TransformBase):

    def __init__(self, params = BoxCoxTransformParams()):
        self.transform_params = params

    def transform(self, series :pd.Series):

        boxcox_result = stats.boxcox(series.values, lmbda=self.transform_params.lmbda, alpha=self.transform_params.alpha)
        #Unpacking result tuple directly from scipy.boxcox(...) causes weird errors in bulk execution of tests!
        res, lmbda = boxcox_result[0], boxcox_result[1]
        self.transform_params.lmbda = lmbda
        return pd.Series(res)

    def inv_transform(self, series :pd.Series):
        return self._inv_boxcox(series, self.transform_params.lmbda)

    #def _boxcox(self,x,lmbda):
    #    if lmbda == 0:
    #        return (np.log(x))

    def _inv_boxcox(self, y, lmbda):
        if lmbda == 0:
            return (np.exp(y))
        return (np.exp(np.log(lmbda * y + 1) / lmbda))

