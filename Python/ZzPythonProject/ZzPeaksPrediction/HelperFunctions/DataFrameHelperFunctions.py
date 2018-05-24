import pandas as pd
import numpy as np

df_normalized_column = "Normalized"
df_predicted_column = "Predicted"


def add_list_to_source_df_padding_overlapping(dataframe, lst, N):
    """As the DFs are splitted with overlapping and results array differ in length, we put N padded elements
    before predicted to fill the gap impeding DF creation."""
    padding = dataframe[df_normalized_column].tolist()[0:N]
    padded_lst = padding
    padded_lst.extend(lst)

    dataframe[df_predicted_column] = pd.Series(padded_lst, dataframe.index)

    actual_predicted_start_timestamp = dataframe.index[N]

    return dataframe, actual_predicted_start_timestamp



def split_df_by_number(dataframe, val_start, test_start, N, train_offset = 2):
    """Consumes DataFrame with Timestamp as Index column and returns
     3 DataFrames corresponding to Train, Validation, Test samples respectively.
     Training DF is returned starting from index 2."""

    total = len(dataframe.index)
    train = dataframe.iloc[train_offset:val_start]
    validation = dataframe.iloc[val_start-N:test_start]
    test = dataframe.iloc[test_start-N:total]

    return train, validation, test


def split_df_by_size(dataframe, val_size, test_size, N, M ):

    total = len(dataframe.index)
    pos_test = int(total * (1 - test_size))
    pos_val = int(pos_test * (1 - val_size))

    return split_df_by_number(dataframe, pos_val, pos_test, N, M)


def generate_data_by_df(dataframe, time_steps, time_shift):
    normalized = dataframe[df_normalized_column].tolist()
    data = np.array(normalized)
    return generate_data(data, time_steps, time_shift)


def generate_data(data, time_steps, time_shift):
    """Consumes Generates input data structure for LSTM NN model"""

    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(dict(a=data[0:len(data) - time_shift], b=data[time_shift:]))

    rnn_x = []
    for i in range(len(data) - time_steps + 1):
        rnn_x.append(data['a'].iloc[i: i + time_steps].as_matrix())
    rnn_x = np.array(rnn_x)

    # Reshape or rearrange the data from row to columns
    # to be compatible with the input needed by the LSTM model
    # which expects 1 float per time point in a given batch
    rnn_x = rnn_x.reshape(rnn_x.shape + (1,))

    rnn_y = data['b'].values
    rnn_y = rnn_y[time_steps - 1:]

    # Reshape or rearrange the data from row to columns
    # to match the input shape
    rnn_y = rnn_y.reshape(rnn_y.shape + (1,))

    return rnn_x, rnn_y