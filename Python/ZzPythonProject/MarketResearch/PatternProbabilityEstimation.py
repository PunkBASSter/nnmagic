import sys
import pandas as pd
import matplotlib.pyplot as plt
import math
import datetime
import numpy as np

#Expected Input file format: "timestamp,open,high,low,close,tick_volume,spread,real_volume\n"

def get_zone(std_cell_list : [], ind_func_res):
    bands_total = std_cell_list.__len__()
    for i in range(0, bands_total):
        if ind_func_res <= std_cell_list[i]:
            return i+1
    return bands_total + 1 if not math.isnan(std_cell_list[bands_total-1]) else math.nan

columns_to_take = ['timestamp', 'open', 'close']
def calc_indicator(path, file_name, ind_value_col, ind_period, bands_period, std_bands):
    print('Filling DataFrame with basic data, Indicator Values, MA, STD')

    data = pd.read_csv(path+file_name)[columns_to_take]
    data['date'] = data.timestamp.apply(datetime.datetime.fromtimestamp)
    data[ind_value_col] = (data.close - data.open).rolling( ind_period).mean()
    data['ma'] = data[ind_value_col].rolling( bands_period ).mean()
    data['std'] = data[ind_value_col].rolling( bands_period ).std()

    print('Calculating Bands of MA+K*STD')
    for k in std_bands:
        data[f'Std_{k}'] = data['ma'] + data['std'].multiply(k)
    std_band_cols = [f'Std_{k}' for k in std_bands] #Bands column headers

    result_df = pd.DataFrame( data[[ind_value_col] + std_band_cols], index=data.index )

    def visualize(df):
        plt.figure()
        df.plot()
    #visualize(result_df)

    print('Defining a zone based on bands where Indicator Value is located')
    result_df['zone'] = result_df.apply( lambda row: get_zone( [row[ki] for ki in std_band_cols], row[ind_value_col] ), axis=1 )
    return result_df

def process_sequences(result_df, sequence_min_len, sequence_max_len, std_bands, ind_period, bands_period):
    print('Processing sequences...')
    final_columns = []
    tmp_dfs = []
    for seq_len in range (sequence_min_len, sequence_max_len+1):
        print(f'Processing with length: {seq_len} of possible {sequence_min_len}-{sequence_max_len} range.')
        seq_cols = [str(c) for c in range( seq_len )]
        seq_cols.reverse()
        for c in seq_cols:
            result_df[c] = result_df['zone'].shift(int(c))
        final_columns = seq_cols
        #zones = range(1, len(std_bands)+2)
        sequence_df = result_df.loc[ind_period -1 + bands_period-1 + seq_len - 1:, seq_cols]
        sequence_df = sequence_df.astype(int)
        plain_df = sequence_df.groupby(seq_cols).size().reset_index(name='count')
        plain_df['prob'] = plain_df['count'].div(sequence_df.__len__())
        tmp_dfs.append(plain_df)

    prob_res = tmp_dfs[tmp_dfs.__len__()-1]
    for df_ix in range(tmp_dfs.__len__()-2,-1,-1):
        prob_res = prob_res.append(tmp_dfs[df_ix], ignore_index=True)

    prob_res = prob_res[final_columns + ['count', 'prob']]
    prob_res = prob_res.fillna(0)
    for c in final_columns:
        prob_res[c] = prob_res[c].astype(int)

    return prob_res

if __name__ == '__main__':
    if len(sys.argv) < 2:
       print("Required config path.")

    ind_df = calc_indicator()

    probability_df = process_sequences(ind_df)

    #elif sys.argv[1] == "c":
    #   pipe_client()
    #else:
    #   print(f"no can do: {sys.argv[1]}")

    print('end')
