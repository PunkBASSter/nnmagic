import numpy as np


def next_batch(x, y, batch_size):
    """get the next batch to process"""

    def as_batch(data, start, count):
        part = []
        for i in range(start, start + count):
            part.append(data[i])
        return np.array(part)

    for i in range(0, len(x)-batch_size, batch_size):
        yield as_batch(x, i, batch_size), as_batch(y, i, batch_size)


def next_value(sample, batch_size=1):
    """get the next batch_size values to evaluate"""

    def as_batch(data, start, count):
        part = []
        for i in range(start, start + count):
            part.append(data[i])
        return np.array(part)

    for i in range(0, len(sample)-batch_size+1, batch_size):
        yield as_batch(sample, i, batch_size)
