import unittest
import pandas as pd
import numpy as np
from DataTransforms.TransformBase import TransformBase, TransformParams
from DataTransforms.BoxCoxTransform import BoxCoxTransform, BoxCoxTransformParams
from DataTransforms.DiffTransform import DiffTransform, DiffTransformParams
from DataTransforms.LogTransform import LogTransform, LogTransformParams
from DataTransforms.ChainedTransform import ChainedTransform

class TestsDataTransform(unittest.TestCase):

    def assertCollectionsEqual(self, series1, series2, msg="Series are not equal, but should.", tolerance = 0.0001):
        lst1 = series1.tolist()
        lst2 = series2.tolist()
        if not len(lst1) == len(lst2):
            raise AssertionError("Series' lengths are not equal.")
        for i in range(0, len(lst1)):
            if abs(series1[i] - series2[i]) > tolerance:
                raise AssertionError(msg)

    def assertCollectionsNotEqual(self, series1, series2, msg="Series are equal, but should not.", tolerance = 0.0001):
        lst1 = series1.tolist()
        lst2 = series2.tolist()
        for i in range(0, len(lst1)):
            if abs(series1[i] - series2[i]) > tolerance:
                return
        raise AssertionError(msg)


    def assertCollectionNotNan(self, collection, msg="Collection contains only NaN values."):
        for item in collection:
            if not item == np.nan and not item is np.nan:
                return
        raise AssertionError(msg)


    def _steps_transform_reverse(self, inst :TransformBase):
        df = pd.DataFrame(data={'Timestamp': [1, 3, 4, 8, 15], 'Value': [2., 4., 8., 16., 32.]})
        df["Transformed"]= inst.transform(df.Value)

        dbg1 = df["Transformed"]
        dbg2 = df.Transformed

        self.assertTrue(len(df.Transformed.tolist())>0, "Transformed sequence length is not greater than 0")
        self.assertCollectionNotNan( df.Transformed )
        self.assertCollectionsNotEqual( df.Value, df.Transformed, "Initial sequence is equal to transformed. Transformation has no effect?")

        df["Restored"] = inst.inv_transform(df.Transformed)

        self.assertCollectionsEqual(df.Value, df.Restored, "Initial sequence is not equal to restored.")

    def _steps_returned_type(self, inst :TransformBase):
        df = pd.DataFrame( data={'Timestamp': [1, 3, 4, 8, 15], 'Value': [2., 4., 8., 16., 32.]} )
        var = inst.transform(df.Value)
        self.assertTrue(isinstance(var, pd.Series))
        var = inst.inv_transform(df.Value)
        self.assertTrue(isinstance(var, pd.Series))

    def test_returned_type_diff(self):
        self._steps_returned_type(DiffTransform())

    def test_returned_type_log(self):
        self._steps_returned_type( LogTransform() )



    def test_tr_chained_diff_log(self):
        self._steps_transform_reverse( ChainedTransform( DiffTransform(), LogTransform() ) )




    def test_tr_diff(self):
        self._steps_transform_reverse(DiffTransform())

    def test_tr_diff_with_nan_replacement(self):
        self._steps_transform_reverse(DiffTransform(DiffTransformParams(nan_replacement_value = 1)))

    def test_tr_log(self):
        self._steps_transform_reverse(LogTransform())


    #Classes dependent on scipy.boxcox(...) fail in bulk test executions if this function is used more than once !!
    #So, only the first executed test of the following will pass!
    def test_tr_boxcox(self):
        self._steps_transform_reverse( BoxCoxTransform() )

    def test_returned_type_boxcox(self):
        self._steps_returned_type( BoxCoxTransform() )

    def test_tr_chained_boxcox_diff(self):
        self._steps_transform_reverse( ChainedTransform( BoxCoxTransform(), DiffTransform() ) )

    def test_tr_chained_boxcox_diff_log(self):
        self._steps_transform_reverse( ChainedTransform( BoxCoxTransform(), DiffTransform(), LogTransform() ) )

if __name__ == '__main__':
    unittest.main()