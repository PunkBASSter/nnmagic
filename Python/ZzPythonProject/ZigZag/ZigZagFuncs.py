import pandas as pd
from FastZigZag import FastZigZag
from DeltaZigZag import DeltaZigZag

def zz_to_levels(ser : pd.Series):
    '''Adds padding of revent ZZ levels to replace zeros.'''
    df = ser.to_frame()
    lvl = df.query( df.columns[0] + ' > 0' )[df.columns[0]].values[0]
    arr = ser.values
    for i in range( 0, arr.__len__() - 1 ):
        arr[i] = lvl
        if arr[i + 1] > 0 and arr[i] != arr[i + 1]:
            lvl = arr[i + 1]
    return pd.Series(arr, ser.index)


def read_csv(file_path, columns_to_take):
    print( f'Trying to read Columns: {columns_to_take} from history CSV {file_path}' )
    data = pd.read_csv( file_path )[columns_to_take]
    return data

if __name__ == '__main__':

    data_path = 'C:/BitBucket/nn_experiments/Python/ZzPythonProject/WrtMarketResearch/Rates_EURUSD_PERIOD_H1.csv'
    rates = read_csv( data_path, ['timestamp', 'open', 'high', 'low', 'close'] )

    fzz = DeltaZigZag(0.03)
    data = rates[['timestamp', 'high', 'low']]
    data1 = rates[['timestamp', 'high', 'low']].loc[:rates.__len__() - 6]

    res1 = fzz.calc_zz(data1)
    res2 = fzz.calc_zz(data)
    res3 = fzz.calc_zz(data)

    print("end")