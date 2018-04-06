import pandas as pd


def split_df_by_number(dataframe, val_start, test_start, N = 25, M = 1):
    """Consumes DataFrame with Timestamp as Index column and returns
     3 DataFrames corresponding to Train, Validation, Test samples respectively."""

    total = dataframe.count()
    train = dataframe.iloc[0:val_start-M]
    validation = dataframe.iloc[val_start-N:test_start]
    test = dataframe.iloc[test_start-N:total]

    return train, validation, test


def split_df_by_size(dataframe, val_size=0.1, test_size=0.2, N = 25, M = 1):

    total = dataframe.count()
    pos_test = int(total * (1 - test_size))
    pos_val = int(pos_test * (1 - val_size))

    return split_df_by_number(dataframe, pos_val, pos_test, N, M)


