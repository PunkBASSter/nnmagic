import pandas as pd
import Normalizers.DiffRatioNormalization as nrm
import HelperFunctions.DataFrameHelperFunctions as dfhf


class DefaultSampleGenerator:

    _normalized_column = "Normalized"
    _index_column = "Timestamp"
    _params = None
    _last_df = None
    _last_train_df = None
    _last_val_df = None
    _last_test_df = None

    def __init__(self, params):
        self._params = params

    def generate_samples(self):
        # Loading, splitting and normalizing data
        print("Loading and preparing raw data.")
        df = pd.read_csv(self._params.io_input_data_file, index_col=self._index_column)
        df.sort_index()

        print("Normalizing data and adding to DataFrame.")
        norm_list, scaling_k = nrm.normalize(df, add_padding=True)
        df[self._normalized_column] = pd.Series(norm_list, df.index)

        n = self._params.pred_N
        m = self._params.pred_M

        print("Splitting DataFrame to Train/Validation/Test samples.")
        df_train, df_val, df_test = dfhf.split_df_by_size(df, self._params.size_validation, self._params.size_test, n,
                                                          nrm.source_offset)

        self._last_df = df
        self._last_train_df = df_train
        self._last_val_df = df_val
        self._last_test_df = df_test

        print("Transforming normalized data from splitted samples to collections with LSTM NN-compatible structure.")
        train__x, train__y = dfhf.generate_data_by_df(df_train, n, m)
        val__x, val__y = dfhf.generate_data_by_df(df_val, n, m)
        test__x, test__y = dfhf.generate_data_by_df(df_test, n, m)

        smp_x = {"train": train__x, "val": val__x, "test": test__x}
        smp_y = {"train": train__y, "val": val__y, "test": test__y}
        return smp_x, smp_y
