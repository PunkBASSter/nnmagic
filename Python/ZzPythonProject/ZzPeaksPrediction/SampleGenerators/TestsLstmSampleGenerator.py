import unittest
import pytest
import pandas as pd
import numpy as np
from SampleGenerators.LstmSampleGenerator import LstmSampleGenerator
from Common.ModelParameters import ModelParameters
from DataTransforms.TransformBase import TransformBase, TransformParams

class TestLstmSampleGenerator(unittest.TestCase):

    input_df = pd.DataFrame([[10, 1], [11, 1.1], [12, 1.2], [13, 1.3]], columns=['Timestamp', 'Value'])
    output_x = np.array([np.array([np.array([1]), np.array([1.1])]), np.array([np.array([1.1]), np.array([1.2])])])
    output_y = np.array([np.array([1.2]), np.array([1.3])])
    _tested_generator : LstmSampleGenerator = None

    def get_tested_instance(self, transform = None) -> LstmSampleGenerator:
        if self._tested_generator:
            return self._tested_generator

        model_params = ModelParameters()
        model_params.pred_N = 2
        model_params.pred_M = 1
        transform = TransformBase(TransformParams()) if not transform else transform
        return LstmSampleGenerator(model_params, transform)

    def test_repack_data_returned_type(self):
        tested_instance = self.get_tested_instance()
        repacked_x, repacked_y = tested_instance.repack_data(self.input_df.Value)

        assert isinstance(repacked_x, np.ndarray), "Returned X value must be of type: np.ndarray."
        assert isinstance(repacked_y, np.ndarray), "Returned Y value must be of type: np.ndarray."

    def test_repack_data_result_shape(self):
        tested_instance = self.get_tested_instance()
        repacked_x, repacked_y = tested_instance.repack_data( self.input_df.Value )

        x_sequence_length = tested_instance._params.pred_N
        y_sequence_length = tested_instance._params.pred_M
        repacked_sequence_len = self.input_df.shape[0] - x_sequence_length - y_sequence_length +1

        assert repacked_x.shape == (repacked_sequence_len, x_sequence_length, 1), "Wrong Shape of repacked X."
        assert repacked_y.shape == (repacked_sequence_len, y_sequence_length), "Wrong Shape of repacked Y."

    def test_generate_sample_by_df(self):
        tested_instance = self.get_tested_instance()
        repacked_x, repacked_y = tested_instance.repack_data( self.input_df.Value )

        assert np.array_equal(repacked_x, self.output_x), "Result X array is not equal to expected."
        assert np.array_equal(repacked_y, self.output_y), "Result Y array is not equal to expected."

