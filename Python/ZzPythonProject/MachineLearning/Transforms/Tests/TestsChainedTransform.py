from Transforms.Tests import TestsDataTransform
from Transforms.BoxCoxTransform import BoxCoxTransform, BoxCoxTransformParams
from Transforms.DiffTransform import DiffTransform, DiffTransformParams
from Transforms.LogTransform import LogTransform, LogTransformParams
from Transforms.ChainedTransform import ChainedTransform


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