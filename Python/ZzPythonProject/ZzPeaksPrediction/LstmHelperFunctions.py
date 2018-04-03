import numpy as np
import cntk.tests.test_utils
cntk.tests.test_utils.set_device_from_pytest_env()


def split_data(data, val_size=0.2, test_size=0.3):
    """splits np.array into training, validation and test"""
    pos_test = int(len(data) * (1 - test_size))
    pos_val = int(len(data[:pos_test]) * (1 - val_size))
    train, val, test = data[:pos_val], data[pos_val:pos_test], data[pos_test:]
    return {"train": train, "val": val, "test": test}

#OLD
def generate_data(data, window_size, forecast_size):
    """generate data unit sequences to feed to rnn"""
    fdlen = len(data)
    rnn_x = []
    rnn_y = []
    for i in range(window_size, fdlen-forecast_size):
        rnn_x.append(np.array(data.iloc[i - window_size:i]))
        rnn_y.append(np.array(data.iloc[i:i + forecast_size]))
    rnn_x = np.array(rnn_x)
    rnn_y = np.array(rnn_y)
    return rnn_x, rnn_y


def next_batch(x, y, data_sample, batch_size):
    """get the next batch to process"""
    def as_batch(data, start, count):
        part = []
        for i in range(start, start + count):
            part.append(data[i])
        return np.array(part)
    for i in range(0, len(x[data_sample])-batch_size, batch_size):
        yield as_batch(x[data_sample], i, batch_size), as_batch(y[data_sample], i, batch_size)


# process batches of 10 days
BATCH_SIZE = 10
def next_batch_seq(x, y, data_sample, batch_size=BATCH_SIZE):
    """get the next batch for training"""

    def as_batch(data, start, count):
        return data[start:start + count]

    for i in range(0, len(x[data_sample]), batch_size):
        yield as_batch(x[data_sample], i, batch_size), as_batch(y[data_sample], i, batch_size)


def generate_data(data, window_size_min, window_size_max, forecast_size):
    """generate data unit sequences to feed to rnn"""
    fdlen = len(data)
    rnn_x = []
    rnn_y = []
    for i in range(window_size_max, fdlen-forecast_size):
        rnn_y.append(data[i:i + forecast_size])
        rnn_x.append(np.array(get_var_sequences(data[i - window_size_max: i], window_size_min)))
    #rnn_x = np.array(rnn_x)
    #rnn_y = np.array(rnn_y)
    return rnn_x, rnn_y


def get_var_sequences(data, start_size=1):
    result = []
    dlen = len(data)
    start = 0 if start_size < 1 else start_size-1
    for i in range(start, dlen):
        result.append(data[dlen-i-1: dlen])
    return result



#def get_var_sequences_test():
#    data = [3, 2, 1, 0]
#    res = get_var_sequences(data, 2)
#    return res

#x = get_var_sequences_test()
#print("fin")
