import pandas as pd
import numpy as np
from DataTransforms.Tests import TestsDataTransform
from DataTransforms.TransformBase import TransformBase, TransformParams
from DataTransforms.BoxCoxTransform import BoxCoxTransform, BoxCoxTransformParams
from DataTransforms.DiffTransform import DiffTransform, DiffTransformParams
from DataTransforms.LogTransform import LogTransform, LogTransformParams
from DataTransforms.ChainedTransform import ChainedTransform


class TestsChainedTransform(TestsDataTransform):

    def test_tr_chained_diff_log(self):
        self._steps_transform_reverse( ChainedTransform( DiffTransform(), LogTransform() ) )

    def test_tr_chained_boxcox_diff(self):
        self._steps_transform_reverse( ChainedTransform( BoxCoxTransform(), DiffTransform() ) )

    def test_tr_chained_boxcox_diff_log(self):
        self._steps_transform_reverse( ChainedTransform( BoxCoxTransform(), DiffTransform(), LogTransform() ) )


