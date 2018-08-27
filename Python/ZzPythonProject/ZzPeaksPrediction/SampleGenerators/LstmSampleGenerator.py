import pandas as pd
import numpy as np
import HelperFunctions.DataFrameHelperFunctions as dfhf
from DataTransforms import TransformBase
from Common.ModelParameters import ModelParameters


class LstmSampleGenerator:
    _transform = None

    _params = None

    samples_cached = None

    results_shift_from_left_df = 0

    def __init__(self, params: ModelParameters, transform: TransformBase):
        self._params = params
        self._transform = transform

    def generate_samples(self):
        # Loading, splitting and normalizing data
        print("Loading and preparing raw data.")
        df = pd.read_csv(self._params.io_input_data_file)
        df.sort_values(by=self._params.data_timestamp_column)

        n = self._params.pred_N
        m = self._params.pred_M
        self.results_shift_from_left_df = n + m - 1

        print("Splitting DataFrame to Train/Validation/Test samples.")
        df_train, df_val, df_test = dfhf.split_df_by_size( df, self._params.data_validation_sample_part, self._params.data_test_sample_part, n, m)

        df_train[self._params.data_normalized_column] = self._transform.transform(df_train[self._params.data_value_column]).values
        df_val[self._params.data_normalized_column] = self._transform.transform(df_val[self._params.data_value_column]).values
        df_test[self._params.data_normalized_column] = self._transform.transform(df_test[self._params.data_value_column]).values

        self.samples_cached = {"train": df_train, "val": df_val, "test": df_test}

        print("Transforming normalized data from splitted samples to collections with LSTM NN-compatible structure.")
        train__x, train__y = dfhf.generate_data_by_df(df_train, n, m)
        val__x, val__y = dfhf.generate_data_by_df(df_val, n, m)
        test__x, test__y = dfhf.generate_data_by_df(df_test, n, m)

        smp_x = {"train": train__x, "val": val__x, "test": test__x}
        smp_y = {"train": train__y, "val": val__y, "test": test__y}
        return smp_x, smp_y

    def window_transform(self, series : pd.Series):
        window_size = self._params.pred_N + self._params.pred_M
        last_start_index = series.__len__() - 

    def add_output_list_to_df(self, lst:list, smp: str):
        sample = self.samples_cached[smp]

        #sample["NnRes"] = pd.Series(lst).values
        #sample["ResInvTransformed"] = self._transform.inv_transform( sample.NnRes ).values

        left_padding = sample[self._params.data_normalized_column].iloc[0: self.results_shift_from_left_df].values
        res_series = pd.Series(lst).iloc[0:].values
        sample["NnRes"] = np.r_[left_padding, res_series]
        sample["ResInvTransformed"] = self._transform.inv_transform(sample["NnRes"]).values
        return sample
