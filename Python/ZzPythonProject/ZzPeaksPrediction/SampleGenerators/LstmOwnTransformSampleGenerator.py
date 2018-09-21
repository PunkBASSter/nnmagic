import pandas as pd
import numpy as np
import HelperFunctions.DataFrameHelperFunctions as dfhf
from DataTransforms.TransformBase import TransformBase
from Common.ModelParameters import ModelParameters
import copy
from time import gmtime, strftime



class LstmOwnTransformSampleGenerator:
    _clean_transform_instance: TransformBase = None
    _last_used_transform: TransformBase = None
    _params: ModelParameters() = None

    def __init__(self, params: ModelParameters, transform: TransformBase):
        self._params = params
        self._clean_transform_instance = transform

    def generate_learning_samples(self) -> [dict, dict]:
        df = self.load_data()
        data = pd.Series(df[self._params.data_value_column])
        train, val, test = self.split_into_samples(data)
        res_x, res_y = {}, {}
        res_x["train"], res_y["train"] = self.generate_nn_input(train)
        res_x["val"], res_y["val"] = self.generate_nn_input(val)
        res_x["test"], res_y["test"] = self.generate_nn_input(test)
        return res_x, res_y

    def load_data(self):
        df = pd.read_csv( self._params.io_input_data_file )
        df.sort_values( by=self._params.data_timestamp_column )
        if not self._validate_df_shape( df ):
            raise ValueError( "Unexpected shape of Input DataFrame." )
        return df
    def _validate_df_shape(self, df: pd.DataFrame) -> bool:
        return df.shape[1] == 2 and df.shape[0] > df.shape[1]

    def generate_nn_input(self, series: pd.Series) -> [np.ndarray, np.ndarray]:
        print( f"Generation for series of {series.__len__()} elements started at:" )
        print( strftime( "%Y-%m-%d %H:%M:%S", gmtime() ) )
        x_len, y_len = self._params.pred_N, self._params.pred_M
        last = series.__len__() - y_len + 1
        rnn_x, rnn_y = [], []
        for i in range(x_len, last):
            self._last_used_transform = copy.deepcopy( self._clean_transform_instance )
            sequence_to_transform = series.loc[i-x_len: i+y_len-1]
            trans_res = self._last_used_transform.transform(sequence_to_transform)
            rnn_x.append(trans_res.loc[0: x_len-1].values)
            rnn_y.append(trans_res.loc[x_len: ].values)

        rnn_x, rnn_y = np.array(rnn_x), np.array(rnn_y)
        rnn_x = rnn_x.reshape(rnn_x.shape + (1,))
        # rnn_y = rnn_y.reshape(rnn_y.shape + (1,))

        print( f"Generation finished at:" )
        print( strftime( "%Y-%m-%d %H:%M:%S", gmtime() ) )
        return rnn_x, rnn_y

    def split_into_samples(self, series: pd.Series) -> [pd.Series, pd.Series, pd.Series]:
        total = len( series.index )
        test_pos = int( total * (1 - self._params.data_test_sample_part) )
        val_pos = int( test_pos * (1 - self._params.data_validation_sample_part) )
        N = self._params.pred_N
        M = self._params.pred_M
        total = series.__len__()
        train = series.iloc[0:val_pos]
        validation = series.iloc[val_pos - N - M:test_pos]
        test = series.iloc[test_pos - N - M:total]
        return train, validation, test

    def interpret_nn_data(self, sequence: pd.Series) -> pd.Series:
        if isinstance(sequence, list):
            sequence = pd.Series(sequence)

        pass
        # todo


