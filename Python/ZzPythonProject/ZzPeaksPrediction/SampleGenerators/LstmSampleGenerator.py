import pandas as pd
import numpy
import HelperFunctions.DataFrameHelperFunctions as dfhf
from DataTransforms import TransformBase
from Common.ModelParameters import ModelParameters


class LstmSampleGenerator:
    _transform = None

    _params = None

    samples_cached_last = None

    _results_shift_from_left = 0

    def __init__(self, params: ModelParameters, transform: TransformBase):
        self._params = params
        self._transform = transform

    def generate_samples(self):
        # Loading, splitting and normalizing data
        print("Loading and preparing raw data.")
        df = pd.read_csv(self._params.io_input_data_file)
        df.sort(self._params.data_timestamp_column)

        #df[self._normalized_column] = self._transform.transform(df[self._value_column]).values

        n = self._params.pred_N
        m = self._params.pred_M
        self._results_shift_from_left = m - 1

        print("Splitting DataFrame to Train/Validation/Test samples.")
        self.samples_cached_last = df_train, df_val, df_test = dfhf.split_df_by_size( df, self._params.data_validation_sample_part, self._params.data_test_sample_part, n, m)

        df_train[self._params.data_normalized_column] = self._transform.transform(df_train[self._params.data_value_column]).values
        df_val[self._params.data_normalized_column] = self._transform.transform(df_val[self._params.data_value_column]).values
        df_test[self._params.data_normalized_column] = self._transform.transform(df_test[self._params.data_value_column]).values

        print("Transforming normalized data from splitted samples to collections with LSTM NN-compatible structure.")
        train__x, train__y = dfhf.generate_data_by_df(df_train, n, m)
        val__x, val__y = dfhf.generate_data_by_df(df_val, n, m)
        test__x, test__y = dfhf.generate_data_by_df(df_test, n, m)

        smp_x = {"train": train__x, "val": val__x, "test": test__x}
        smp_y = {"train": train__y, "val": val__y, "test": test__y}
        return smp_x, smp_y
