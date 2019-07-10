import pandas as pd
import numpy as np
import pytest
from DataTransforms.Tests import TestsDataTransform
from DataTransforms.TransformBase import TransformBase, TransformParams
from DataTransforms.BoxCoxTransform import BoxCoxTransform, BoxCoxTransformParams
from DataTransforms.DiffTransform import DiffTransform, DiffTransformParams
from DataTransforms.LogTransform import LogTransform, LogTransformParams
from DataTransforms.ChainedTransform import ChainedTransform


#not used :( doesn't work in test runs
class TestsChainedTransform(TestsDataTransform):

    def test_tr_chained_diff_log(self):
        self._steps_transform_reverse( ChainedTransform( DiffTransform(DiffTransformParams()),
                                                         LogTransform(LogTransformParams()) ) )

    def test_tr_chained_boxcox_diff(self):
        self._steps_transform_reverse( ChainedTransform( BoxCoxTransform(BoxCoxTransformParams()),
                                                         DiffTransform(DiffTransformParams()) ) )

    def test_tr_chained_boxcox_diff_log(self):
        self._steps_transform_reverse( ChainedTransform( BoxCoxTransform(BoxCoxTransformParams()),
                                                         DiffTransform(DiffTransformParams()),
                                                         LogTransform(LogTransformParams()) ) )


#if __name__ == '__main__':
#    unittest.main()