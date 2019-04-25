import unittest
import pandas as pd
import numpy as np
import math
from DataTransforms.TransformBase import TransformBase
from DataTransforms.BoxCoxTransform import BoxCoxTransform
from DataTransforms.DiffTransform import DiffTransform
from DataTransforms.DivisionTransform import DivisionTransform
from DataTransforms.LogTransform import LogTransform
from DataTransforms.ValueShiftTransform import ValueShiftTransform
from DataTransforms.ValueScaleTransform import ValueScaleTransform
from DataTransforms.ChainedTransform import ChainedTransform


class TestsDataTransform(unittest.TestCase):

    # Custom sequenceXY assertions
    def assertCollectionsEqual(self, series1, series2, msg="Series are not equal, but should.", tolerance=0.0001):
        lst1 = series1.tolist()
        lst2 = series2.tolist()
        if not len(lst1) == len(lst2):
            raise AssertionError("Series' lengths are not equal.")
        for i in range(0, len(lst1)):
            if abs(lst1[i] - lst2[i]) > tolerance:
                raise AssertionError(msg)

    def assertCollectionsNotEqual(self, series1, series2, msg="Series are equal, but should not.", tolerance=0.0001):
        lst1 = series1.tolist()
        lst2 = series2.tolist()
        for i in range(0, len(lst1)):
            if abs(series1[i] - series2[i]) > tolerance:
                return
        raise AssertionError(msg)

    def assertCollectionNotNan(self, collection, msg="Collection contains only NaN values."):
        for item in collection:
            if not math.isnan(item):
                return
        raise AssertionError(msg)

    def _steps_transform(self, inst: TransformBase, value_data, expected_data):
        inputs = pd.Series(value_data)
        outputs = inst.transform(inputs)
        expected = pd.Series(expected_data)
        self.assertCollectionNotNan(outputs)
        self.assertCollectionsEqual(outputs, expected, "Incorrect transform result.")

    def _steps_inv_transform(self, inst: TransformBase, value_data, expected_data):
        inputs = pd.Series(value_data)
        outputs = inst.inv_transform(inputs)
        expected = pd.Series(expected_data)
        self.assertCollectionNotNan(outputs)
        self.assertCollectionsEqual(outputs, expected, "Incorrect transform result.")

    # Shared Test Steps
    def _steps_transform_reverse(self, inst: TransformBase, value_data):
        df = pd.DataFrame(data={'Timestamp': [1, 3, 4, 8, 15], 'Value': value_data})
        df["Transformed"] = inst.transform(df.Value)

        self.assertTrue(len(df.Transformed.tolist()) > 0, "Transformed sequenceXY length is not greater than 0")
        self.assertCollectionNotNan(df.Transformed)

        self.assertCollectionsNotEqual(df.Value, df.Transformed,
                                       "Initial sequenceXY is equal to transformed. Transformation has no effect?")

        df["Restored"] = inst.inv_transform(df.Transformed)
        self.assertCollectionsEqual(df.Value, df.Restored, "Initial sequenceXY is not equal to restored.")

    def _steps_returned_type(self, inst: TransformBase):
        df = pd.DataFrame(data={'Timestamp': [1, 3, 4, 8, 15], 'Value': [2., 4., 8., 16., 32.]})
        var = inst.transform(df.Value)
        self.assertTrue(isinstance(var, pd.Series))
        var = inst.inv_transform(df.Value)
        self.assertTrue(isinstance(var, pd.Series))

    # unit tests for returned types
    def test_returned_type_diff(self):
        self._steps_returned_type(DiffTransform())

    def test_returned_type_division(self):
        self._steps_returned_type(DivisionTransform())

    def test_returned_type_log(self):
        self._steps_returned_type(LogTransform())

    def test_returned_type_shift(self):
        self._steps_returned_type(ValueShiftTransform())

    def test_returned_type_scalse(self):
        self._steps_returned_type(ValueScaleTransform())

    # transform classes unit tests
    def test_transform_diff(self):
        self._steps_transform(DiffTransform(), [2., 4., 8., 16., 32.], [np.NaN, 2., 4., 8., 16.])

    def test_inv_transform_diff(self):
        dt = DiffTransform()
        dt.last_input_series = pd.Series([2., 4., 8., 16., 32.])
        self._steps_inv_transform(dt, [np.NaN, 2., 4., 8., 16., 32], [2., 4., 8., 16., 32., 64])

    def test_tr_diff(self):
        self._steps_transform_reverse(DiffTransform(), [2., 4., 8., 16., 32.])

    #def test_division

    def test_transform_division(self):
        self._steps_transform(DivisionTransform(),
                              [np.NaN, 2., 4., 8., 16.], [np.NaN, np.NaN, 2., 2., 2.])

    def test_inv_transform_division(self):
        dt = DivisionTransform()
        dt.last_input_series = pd.Series([np.NaN, 2., 4., 8., 16.])
        self._steps_inv_transform(dt, [np.NaN, np.NaN, 2., 2., 2., 2.], [np.NaN, 2., 4., 8., 16., 32])

    def test_tr_division(self):
        self._steps_transform_reverse(DivisionTransform(), [np.NaN, 2.0, -12., -8., 20.])

    def test_tr_shift(self):
        self._steps_transform_reverse(ValueShiftTransform(), [2., 4., -8., -16., 32.])

    def test_transform_log(self):
        self._steps_transform(LogTransform(), [np.NaN, 2, 1, 2], [np.NaN, 1, 0, 1])

    def test_tr_log(self):
        self._steps_transform_reverse(LogTransform(), [2., 4., 5., 0.5, 3.])

    def test_tr_boxcox(self):
        self._steps_transform_reverse(BoxCoxTransform(), [2., 4., 8., 16., 32.])

    def test_tr_scale(self):
        self._steps_transform_reverse(ValueScaleTransform(), [2., 4., -8., 16., 32.])

    # integration tests
    def test_chained_diff_div(self):
        diff_transform = DiffTransform()
        div_transform = DivisionTransform()
        self._steps_transform( ChainedTransform( diff_transform, div_transform ), [2., 4., 8., 16., 32.],
                               [np.NaN, np.NaN, 2., 2., 2.] )

    def test_inv_chained_diff_div(self):
        diff_transform = DiffTransform()
        diff_transform.last_input_series = pd.Series( [2., 4., 8., 16., 32.] )
        div_transform = DivisionTransform()
        div_transform.last_input_series = pd.Series( [np.NaN, 2., 4., 8., 16.] )
        self._steps_inv_transform(ChainedTransform (diff_transform, div_transform), [np.NaN, np.NaN, 2., 2., 2., 2],
                                      [2., 4., 8., 16., 32., 64])

    def test_tr_chained_diff_shift_log(self):
        self._steps_transform_reverse(ChainedTransform(DiffTransform(),
                                                       ValueShiftTransform(),
                                                       LogTransform()),
                                      [2., 4., 8., 16., 32.])

    def test_tr_chained_diff_shiftNegative_log(self):
        self._steps_transform_reverse(ChainedTransform(DiffTransform(),
                                                       ValueShiftTransform(),
                                                       LogTransform()),
                                      [2., -4., 8., -16., 9.])

    def test_returned_type_boxcox(self):
        self._steps_returned_type(BoxCoxTransform())

    def test_tr_chained_boxcox_diff(self):
        self._steps_transform_reverse(ChainedTransform(BoxCoxTransform(),
                                                       DiffTransform()),
                                      [2., 4., 8., 16., 32.])

    def test_tr_chained_boxcox_diff_log(self):
        self._steps_transform_reverse(ChainedTransform(DiffTransform(),
                                                       ValueShiftTransform(),
                                                       BoxCoxTransform()),
                                      [2., 4., -8., -16., 4.])

    def test_tr_chained_diff_scale_shift(self):
        self._steps_transform_reverse(ChainedTransform(DiffTransform(),
                                                       ValueScaleTransform(),
                                                       ValueShiftTransform()),
                                      [2., 4., -8., -16., 4.])

    def test_tr_chained_diff_division(self):
        self._steps_transform_reverse(ChainedTransform(DiffTransform(),
                                                       DivisionTransform()),
                                      [2., 4., -8., -16., 4.])

    def test_tr_chained_division_log(self):
        self._steps_transform_reverse(ChainedTransform(DivisionTransform(),
                                                       LogTransform()),
                                      [np.NaN, 2.0, 12., 8., 20.])

    def test_tr_chained_diff_division_shift_scale_log(self):
        self._steps_transform_reverse(ChainedTransform(DiffTransform(),
                                                       DivisionTransform(),
                                                       ValueShiftTransform(),
                                                       LogTransform()),
                                      [2., 4., -8., -16., 4.])


if __name__ == '__main__':
    unittest.main()
