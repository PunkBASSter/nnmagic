import unittest
import pandas as pd
import numpy as np
from DataTransforms.TransformBase import TransformBase, TransformParams
from DataTransforms.BoxCoxTransform import BoxCoxTransform, BoxCoxTransformParams
from DataTransforms.DiffTransform import DiffTransform, DiffTransformParams
from DataTransforms.LogTransform import LogTransform, LogTransformParams
from DataTransforms.ShiftToPositiveTransform import ShiftToPositiveTransform, ShiftToPositiveTransformParams
from DataTransforms.ChainedTransform import ChainedTransform

class TestsDataTransform(unittest.TestCase):

    #Custom sequence assertions
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


    #Shared Test Steps
    def _steps_transform_reverse(self, inst :TransformBase, value_data):
        df = pd.DataFrame(data={'Timestamp': [1, 3, 4, 8, 15], 'Value': value_data})
        df["Transformed"]= inst.transform(df.Value)

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


    #Test cases
    def test_returned_type_diff(self):
        self._steps_returned_type(DiffTransform(DiffTransformParams()))

    def test_returned_type_log(self):
        self._steps_returned_type( LogTransform(LogTransformParams()) )

    def test_returned_type_shift(self):
        self._steps_returned_type(ShiftToPositiveTransform(ShiftToPositiveTransformParams()))

    #WARNING! ONLY First executed ChainedTransform Test Case passes!
    def test_tr_chained_diff_shift_log(self):
        self._steps_transform_reverse( ChainedTransform( DiffTransform(DiffTransformParams()), ShiftToPositiveTransform(ShiftToPositiveTransformParams()), LogTransform(LogTransformParams())), [2., 4., 8., 16., 32.])
    def test_tr_chained_diff_shiftNegative_log(self):
        self._steps_transform_reverse( ChainedTransform( DiffTransform(DiffTransformParams()), ShiftToPositiveTransform(ShiftToPositiveTransformParams()), LogTransform(LogTransformParams())), [2., -4., 8., -16., 9.])

    def test_tr_diff(self):
        self._steps_transform_reverse(DiffTransform(DiffTransformParams()), [2., 4., 8., 16., 32.])
    def test_tr_diff_with_nan_replacement(self):
        self._steps_transform_reverse(DiffTransform(DiffTransformParams(nan_replacement_value = 1)), [2., 4., 8., 16., 32.])

    def test_tr_shift(self):
        self._steps_transform_reverse(ShiftToPositiveTransform(ShiftToPositiveTransformParams()), [2., 4., -8., -16., 32.])

    def test_tr_log(self):
        self._steps_transform_reverse(LogTransform(LogTransformParams()), [2., 4., 8., 16., 32.])

    def test_tr_logNegative(self):
        self._steps_transform_reverse(LogTransform(LogTransformParams()), [2., -4., 8., 16., -32.])

    def test_tr_boxcox(self):
        self._steps_transform_reverse( BoxCoxTransform(BoxCoxTransformParams()), [2., 4., 8., 16., 32.] )
#
    def test_returned_type_boxcox(self):
        self._steps_returned_type( BoxCoxTransform(BoxCoxTransformParams()))
#
    def test_tr_chained_boxcox_diff(self):
        self._steps_transform_reverse( ChainedTransform( BoxCoxTransform(BoxCoxTransformParams()), DiffTransform(DiffTransformParams()) ), [2., 4., 8., 16., 32.] )

    def test_tr_chained_boxcox_diff_log(self):
        self._steps_transform_reverse( ChainedTransform(DiffTransform(DiffTransformParams()), ShiftToPositiveTransform(ShiftToPositiveTransformParams()), BoxCoxTransform(BoxCoxTransformParams())),[2., 4., -8., -16., 4.])

if __name__ == '__main__':
    unittest.main()