import unittest
import pandas as pd
import numpy as np
import math
from DataTransforms.TransformBase import TransformBase, TransformParams
from DataTransforms.BoxCoxTransform import BoxCoxTransform, BoxCoxTransformParams
from DataTransforms.DiffTransform import DiffTransform, DiffTransformParams
from DataTransforms.DivisionTransform import DivisionTransform, DivisionTransformParams
from DataTransforms.LogTransform import LogTransform, LogTransformParams
from DataTransforms.ValueShiftTransform import ValueShiftTransform, ValueShiftTransformParams
from DataTransforms.ValueScaleTransform import ValueScaleTransform, ValueScaleTransformParams
from DataTransforms.ChainedTransform import ChainedTransform


class TestsDataTransform(unittest.TestCase):

    # Custom sequence assertions
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

        self.assertTrue(len(df.Transformed.tolist()) > 0, "Transformed sequence length is not greater than 0")
        self.assertCollectionNotNan(df.Transformed)

        self.assertCollectionsNotEqual(df.Value, df.Transformed,
                                       "Initial sequence is equal to transformed. Transformation has no effect?")

        df["Restored"] = inst.inv_transform(df.Transformed)
        self.assertCollectionsEqual(df.Value, df.Restored, "Initial sequence is not equal to restored.")

    def _steps_returned_type(self, inst: TransformBase):
        df = pd.DataFrame(data={'Timestamp': [1, 3, 4, 8, 15], 'Value': [2., 4., 8., 16., 32.]})
        var = inst.transform(df.Value)
        self.assertTrue(isinstance(var, pd.Series))
        var = inst.inv_transform(df.Value)
        self.assertTrue(isinstance(var, pd.Series))

    # unit tests for returned types
    def test_returned_type_diff(self):
        self._steps_returned_type(DiffTransform(DiffTransformParams()))

    def test_returned_type_division(self):
        self._steps_returned_type(DivisionTransform(DivisionTransformParams()))

    def test_returned_type_log(self):
        self._steps_returned_type(LogTransform(LogTransformParams()))

    def test_returned_type_shift(self):
        self._steps_returned_type(ValueShiftTransform(ValueShiftTransformParams()))

    def test_returned_type_scalse(self):
        self._steps_returned_type(ValueScaleTransform(ValueScaleTransformParams()))

    # transform classes unit tests
    def test_transform_diff(self):
        self._steps_transform(DiffTransform(DiffTransformParams()), [2., 4., 8., 16., 32.], [np.NaN, 2., 4., 8., 16.])

    def test_inv_transform_diff(self):
        initial_sequence = [2., 4., 8., 16., 32.]
        params = DiffTransformParams()
        params.last_input_series = pd.Series(initial_sequence)
        self._steps_inv_transform(DiffTransform(params), [np.NaN, 2., 4., 8., 16.], initial_sequence)

    def test_tr_diff(self):
        self._steps_transform_reverse(DiffTransform(DiffTransformParams()), [2., 4., 8., 16., 32.])

    #def test_division

    def test_transform_division(self):
        self._steps_transform(DivisionTransform(DivisionTransformParams()),
                              [np.NaN, 2., 4., 8., 16.], [np.NaN, np.NaN, 2., 2., 2.])

    def test_inv_transform_division(self):
        initial_sequence = [np.NaN, 2., 4., 8., 16.]
        params = DivisionTransformParams()
        params.last_input_series = pd.Series(initial_sequence)
        self._steps_inv_transform(DivisionTransform(params), [np.NaN, np.NaN, 2., 2., 2.], initial_sequence)

    def test_tr_division(self):
        self._steps_transform_reverse(DivisionTransform(DivisionTransformParams()), [np.NaN, 2.0, -12., -8., 20.])

    def test_tr_shift(self):
        self._steps_transform_reverse(ValueShiftTransform(ValueShiftTransformParams()), [2., 4., -8., -16., 32.])

    def test_transform_log(self):
        self._steps_transform(LogTransform(LogTransformParams()), [np.NaN, 2, 1, 2], [np.NaN, 1, 0, 1])

    def test_tr_log(self):
        self._steps_transform_reverse(LogTransform(LogTransformParams()), [2., 4., 5., 0.5, 3.])

    def test_tr_boxcox(self):
        self._steps_transform_reverse(BoxCoxTransform(BoxCoxTransformParams()), [2., 4., 8., 16., 32.])

    def test_tr_scale(self):
        self._steps_transform_reverse(ValueScaleTransform(ValueScaleTransformParams()), [2., 4., -8., 16., 32.])

    # integration tests
    def test_tr_chained_diff_shift_log(self):
        self._steps_transform_reverse(ChainedTransform(DiffTransform(DiffTransformParams()),
                                                       ValueShiftTransform(ValueShiftTransformParams()),
                                                       LogTransform(LogTransformParams())),
                                      [2., 4., 8., 16., 32.])

    def test_tr_chained_diff_shiftNegative_log(self):
        self._steps_transform_reverse(ChainedTransform(DiffTransform(DiffTransformParams()),
                                                       ValueShiftTransform(ValueShiftTransformParams()),
                                                       LogTransform(LogTransformParams())),
                                      [2., -4., 8., -16., 9.])

    def test_returned_type_boxcox(self):
        self._steps_returned_type(BoxCoxTransform(BoxCoxTransformParams()))

    def test_tr_chained_boxcox_diff(self):
        self._steps_transform_reverse(ChainedTransform(BoxCoxTransform(BoxCoxTransformParams()),
                                                       DiffTransform(DiffTransformParams())),
                                      [2., 4., 8., 16., 32.])

    def test_tr_chained_boxcox_diff_log(self):
        self._steps_transform_reverse(ChainedTransform(DiffTransform(DiffTransformParams()),
                                                       ValueShiftTransform(ValueShiftTransformParams()),
                                                       BoxCoxTransform(BoxCoxTransformParams())),
                                      [2., 4., -8., -16., 4.])

    def test_tr_chained_diff_scale_shift(self):
        self._steps_transform_reverse(ChainedTransform(DiffTransform(DiffTransformParams()),
                                                       ValueScaleTransform(ValueScaleTransformParams()),
                                                       ValueShiftTransform(ValueShiftTransformParams())),
                                      [2., 4., -8., -16., 4.])

    def test_tr_chained_diff_division(self):
        self._steps_transform_reverse(ChainedTransform(DiffTransform(DiffTransformParams()),
                                                       DivisionTransform(DivisionTransformParams())),
                                      [2., 4., -8., -16., 4.])

    def test_tr_chained_division_log(self):
        self._steps_transform_reverse(ChainedTransform(DivisionTransform(DivisionTransformParams()),
                                                       LogTransform(LogTransformParams())),
                                      [np.NaN, 2.0, 12., 8., 20.])

    def test_tr_chained_diff_division_shift_scale_log(self):
        self._steps_transform_reverse(ChainedTransform(DiffTransform(DiffTransformParams()),
                                                       DivisionTransform(DivisionTransformParams()),
                                                       ValueShiftTransform(ValueShiftTransformParams()),
                                                       LogTransform(LogTransformParams())),
                                      [2., 4., -8., -16., 4.])


if __name__ == '__main__':
    unittest.main()
