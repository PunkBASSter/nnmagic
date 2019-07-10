import pandas as pd
import numpy as np
from TransformBase import TransformBase
import copy
from time import gmtime, strftime


class LstmOwnTransformSampleGenerator:
    clean_transform_instance: TransformBase = None
    data_frame: pd.DataFrame = None
    _last_used_transform: TransformBase = None

    test_sample_series: pd.Series = None

    def __init__(self, params, transform: TransformBase):
        self._params = params
        self.clean_transform_instance = transform
        self._params = None

    def generate_learning_samples(self) -> (dict, dict):
        df = self.load_data()
        data = pd.Series(df[self._params.data_value_column])
        train, val, test = self.split_into_samples(data)
        #For further testing:
        self.test_sample_series = test
        res_x, res_y = {}, {}
        res_x["train"], res_y["train"] = self.generate_nn_input(train)
        res_x["val"], res_y["val"] = self.generate_nn_input(val)
        res_x["test"], res_y["test"] = self.generate_nn_input(test)
        return res_x, res_y

    def load_data(self):
        df = pd.read_csv(self._params.io_input_data_file)
        df.sort_values(by=self._params.data_timestamp_column)
        if not self._validate_df_shape( df ):
            raise ValueError( "Unexpected shape of Input DataFrame." )
        self.data_frame = df
        return df
    def _validate_df_shape(self, df: pd.DataFrame) -> bool:
        return df.shape[1] == 2 and df.shape[0] > df.shape[1]

#TODO GENERATE WHOLE SEQUENCE AND ONLY THEN SPLIT INTO X and Y
    def generate_nn_input(self, series: pd.Series) -> (np.ndarray, np.ndarray):
        print( f"Generation for series of {series.__len__()} elements started at:" )
        print( strftime( "%Y-%m-%d %H:%M:%S", gmtime() ) )
        x_len, y_len = self._params.pred_N, self._params.pred_M
        data = pd.Series(series.values)
        last = data.__len__() - y_len + 1
        rnn_x, rnn_y = [], []
        for i in range(x_len, last):
            self._last_used_transform = copy.deepcopy(self.clean_transform_instance)
            sequence_to_transform = data.loc[i-x_len: i+y_len-1]
            trans_res = self._last_used_transform.transform(sequence_to_transform)
            rnn_x.append(trans_res.loc[: x_len-1].values.astype(np.float32))
            rnn_y.append(trans_res.loc[x_len: ].values.astype(np.float32))
            #DBG
            #debug_nans_restore = self._last_used_transform.inv_transform(trans_res)

        rnn_x, rnn_y = np.array(rnn_x), np.array(rnn_y)
        rnn_x = rnn_x.reshape(rnn_x.shape + (1,))
        # rnn_y = rnn_y.reshape(rnn_y.shape + (1,))

        print( f"Generation finished at:" )
        print( strftime( "%Y-%m-%d %H:%M:%S", gmtime() ) )
        return rnn_x, rnn_y

    def generate_nn_input_X(self, array: np.array) -> (np.ndarray, np.array):
        self._last_used_transform = copy.deepcopy( self.clean_transform_instance )
        as_array_x = self._last_used_transform.transform(pd.Series(array)).values
        input_x = [as_array_x.copy()]
        input_x = np.array(input_x)
        input_x = input_x.reshape(input_x.shape + (1,))
        # rnn_y = rnn_y.reshape(rnn_y.shape + (1,))
        return input_x.astype(np.float32), as_array_x

    def generate_test_input_sequences(self, series: pd.Series) -> []:
        x_len, y_len = self._params.pred_N, self._params.pred_M
        data = pd.Series(series.values)
        last = data.__len__() - y_len + 1
        test_x, test_y = [], []
        for i in range( x_len, last ):
            test_x.append( data.loc[i - x_len: i-1].values.astype(np.float32) )
            test_y.append(data.loc[i: i + y_len-1].values.astype(np.float32)[0]) #TODO КАСТЫЛЬ С 1< РАЗМЕРНОСТЬЮ
        return test_x, test_y

    def split_into_samples(self, series: pd.Series) -> [pd.Series, pd.Series, pd.Series]:
        total = len( series.index )
        test_pos = int( total * (1 - self._params.data_test_sample_part) )
        val_pos = int( test_pos * (1 - self._params.data_validation_sample_part) )
        N = self._params.pred_N
        M = self._params.pred_M
        total = series.__len__()
        train = series.loc[0:val_pos]
        validation = series.loc[val_pos - N - M:test_pos]
        test = series.loc[test_pos - N - M:total]
        return train, validation, test

    def interpret_nn_data(self, sequence: pd.Series) -> pd.Series:
        if isinstance(sequence, list):
            sequence = pd.Series(sequence)

        pass
        # todo
