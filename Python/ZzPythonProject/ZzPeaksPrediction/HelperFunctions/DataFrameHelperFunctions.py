import pandas as pd
import numpy as np

df_normalized_column = "Normalized"

def split_df_by_number(dataframe, val_start, test_start, N = 25, M = 1):
    """Consumes DataFrame with Timestamp as Index column and returns
     3 DataFrames corresponding to Train, Validation, Test samples respectively."""

    total = dataframe.count()
    train = dataframe.iloc[0:val_start]
    validation = dataframe.iloc[val_start-N:test_start]
    test = dataframe.iloc[test_start-N:total]

    return train, validation, test


def split_df_by_size(dataframe, val_size=0.1, test_size=0.2, N = 25, M = 1):

    total = dataframe.count()
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