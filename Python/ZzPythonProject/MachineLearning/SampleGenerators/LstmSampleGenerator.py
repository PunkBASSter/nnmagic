import pandas as pd
import numpy as np
import DataFrameHelperFunctions as dfhf
from DataTransforms.TransformBase import TransformBase
from Common.ModelParameters import ModelParameters
import copy


class LstmSampleGenerator:
    _clean_transform_instance: TransformBase = None
    _last_used_transform: TransformBase = None
    _params: ModelParameters() = None

    def __init__(self, params: ModelParameters, transform: TransformBase):
        self._params = params
        self._clean_transform_instance = transform

    def generate_samples(self):
        # Loading, splitting and normalizing data
        df = self.load_data()

        n = self._params.pred_N
        m = self._params.pred_M

        df_train, df_val, df_test = \
            dfhf.split_df_by_size(df, self._params.data_validation_sample_part, self._params.data_test_sample_part, n, m)

        df_train[self._params.data_normalized_column] = self._clean_transform_instance.transform(df_train[self._params.data_value_column]).values
        df_val[self._params.data_normalized_column] = self._clean_transform_instance.transform(df_val[self._params.data_value_column]).values
        df_test[self._params.data_normalized_column] = self._clean_transform_instance.transform(df_test[self._params.data_value_column]).values

        train__x, train__y = dfhf.generate_data_by_df(df_train, n, m)
        val__x, val__y = dfhf.generate_data_by_df(df_val, n, m)
        test__x, test__y = dfhf.generate_data_by_df(df_test, n, m)

        smp_x = {"train": train__x, "val": val__x, "test": test__x}
        smp_y = {"train": train__y, "val": val__y, "test": test__y}
        return smp_x, smp_y

    def generate_with_own_transform(self):
        df = self.load_data()
        data = pd.Series(df[self._params.data_value_column])

        pre_res = self.compose_sample_from_raw_data(data)

        return pre_res

    def load_data(self):
        df = pd.read_csv( self._params.io_input_data_file )
        df.sort_values( by=self._params.data_timestamp_column )
        if not self._validate_df_shape( df ):
            raise ValueError( "Unexpected shape of Input DataFrame." )
        return df
    def _validate_df_shape(self, df: pd.DataFrame) -> bool:
        return df.shape[1] == 2 and df.shape[0] > df.shape[1]

    #TODO Merge COMPOSE methods based on passed transform
    def compose_sample_from_prepared_data(self, series: pd.Series) -> [np.ndarray, np.ndarray]:
        """
        Composes LSTM-compatible input data structures extracted from normalized (prepared) series.
        """
        x_len, y_len = self._params.pred_N, self._params.pred_M

        last = series.__len__() - y_len + 1
        rnn_x, rnn_y = [], []
        for i in range( x_len, last ):
            rnn_x.append( series.iloc[i - x_len: i].values )
            rnn_y.append( series.iloc[i: i + y_len].values )

        rnn_x, rnn_y = np.array( rnn_x ), np.array( rnn_y )
        rnn_x = rnn_x.reshape( rnn_x.shape + (1,) )
        # rnn_y = rnn_y.reshape(rnn_y.shape + (1,))
        return rnn_x, rnn_y

    def compose_sample_from_raw_data(self, series: pd.Series) -> [np.ndarray, np.ndarray]:
        """
        Extracts LSTM-compatible input data structures from raw data performing transformation of each one
        individually. Saves the last used transformation to allow the reverse operation.
        """
        x_len, y_len = self._params.pred_N, self._params.pred_M

        last = series.__len__() - y_len + 1
        rnn_x, rnn_y = [], []
        self._last_used_transform = copy.deepcopy(self._clean_transform_instance)
        for i in range(x_len, last):
            trans_res = self._last_used_transform.transform(series.iloc[i-x_len: i+y_len])
            rnn_x.append( trans_res.iloc[i - x_len: i].values )
            rnn_y.append( trans_res.iloc[i: i + y_len].values )

        rnn_x, rnn_y = np.array(rnn_x), np.array(rnn_y)
        rnn_x = rnn_x.reshape(rnn_x.shape + (1,))
        # rnn_y = rnn_y.reshape(rnn_y.shape + (1,))
        return rnn_x, rnn_y

    def interpret_nn_data(self, sequence: pd.Series) -> pd.Series:
        if isinstance(sequence, list):
            sequence = pd.Series(sequence)

        pass
        # todo

    def add_output_list_to_df(self, lst:list, smp: str):
        sample = self.samples_cached[smp]

        left_padding = sample[self._params.data_normalized_column].iloc[0: self.results_shift_from_left_df].values
        res_series = pd.Series(lst).iloc[0:].values
        sample["NnRes"] = np.r_[left_padding, res_series]
        sample["ResInvTransformed"] = self._clean_transform_instance.inv_transform(sample["NnRes"]).values
        return sample
