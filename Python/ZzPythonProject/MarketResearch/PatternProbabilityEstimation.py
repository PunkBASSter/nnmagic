import sys
import pandas as pd
import matplotlib.pyplot as plt
import math
import datetime
import numpy as np
import json

#Expected Input file format: "timestamp,open,high,low,close,tick_volume,spread,real_volume\n"

def get_zone(std_cell_list : [], ind_func_res):
    bands_total = std_cell_list.__len__()
    for i in range(0, bands_total):
        if ind_func_res <= std_cell_list[i]:
            return i+1
    return bands_total + 1 if not math.isnan(std_cell_list[bands_total-1]) else math.nan

def read_csv(file_path, columns_to_take):
    print(f'Trying to read Columns: {columns_to_take} from history CSV {file_path}')
    data = pd.read_csv( file_path )[columns_to_take]
    return data

def calc_indicator(data, ind_value_col, ind_period, bands_period, std_bands):
    print('Filling DataFrame with basic data, Indicator Values, MA, STD')

    data['date'] = data.timestamp.apply(datetime.datetime.fromtimestamp)
    data[ind_value_col] = (data.close - data.open).rolling( ind_period ).mean()
    data['ma'] = data[ind_value_col].rolling( bands_period ).mean()
    data['std'] = data[ind_value_col].rolling( bands_period ).std()

    print('Calculating Bands of MA+K*STD')
    for k in std_bands:
        data[f'Std_{k}'] = data['ma'] + data['std'].multiply(k)
    std_band_cols = [f'Std_{k}' for k in std_bands] #Bands column headers

    visual_df = pd.DataFrame( data[[ind_value_col] + std_band_cols], index=data.index )

    print('Defining a zone based on bands where Indicator Value is located')
    zoned_df = pd.DataFrame( visual_df )
    zoned_df['zone'] = zoned_df.apply( lambda row: get_zone( [row[ki] for ki in std_band_cols], row[ind_value_col] ), axis=1 )
    #add timestamps to zoned_df here
    return zoned_df, visual_df

def process_sequences(inp_df, sequence_min_len, sequence_max_len, ind_period, bands_period):
    print('Processing sequences...')
    final_columns = []
    tmp_dfs = []
    for seq_len in range (sequence_min_len, sequence_max_len+1):
        print(f'Processing with length: {seq_len} of possible {sequence_min_len}-{sequence_max_len} range.')
        seq_cols = [f'Seq_{c}' for c in range( seq_len )]
        #seq_cols.reverse()
        for i in range(seq_cols.__len__()):
            inp_df[seq_cols[i]] = pd.Series(inp_df['zone']).shift(i)
        final_columns = seq_cols
        #zones = range(1, len(std_bands)+2)
        sequence_df = inp_df.loc[ind_period - 1 + bands_period - 1 + seq_len - 1:, seq_cols]
        sequence_df = sequence_df.astype(int)
        plain_df = sequence_df.groupby(seq_cols).size().reset_index(name='count')
        plain_df['prob'] = plain_df['count'].div(sequence_df.__len__())
        tmp_dfs.append(plain_df)

    prob_res = tmp_dfs[tmp_dfs.__len__()-1]
    for df_ix in range(tmp_dfs.__len__()-2,-1,-1):
        prob_res = prob_res.append(tmp_dfs[df_ix], ignore_index=True)

    final_columns.reverse()
    prob_res = prob_res[final_columns + ['count', 'prob']]
    prob_res = prob_res.fillna(0)
    for c in final_columns:
        prob_res[c] = prob_res[c].astype(int)

    return prob_res



if __name__ == '__main__':
    settings_file_name = "Settings.json"
    if len(sys.argv) > 1:
        settings_file_name = sys.argv[1]
    else:
        print("Taking default settings file")

    with open(settings_file_name, 'r') as f:
        config = json.load(f)

    input_folder = config["input_folder"] # C:\\Users\\PunkBASSter\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\
    file_name = config["file_name"]
    columns_to_take = config["columns_to_take"]
    output_folder = config["output_folder"]
    out_file_name_prefix = config["out_file_name_prefix"]
    calculations_file_name_prefix = config["calculations_file_name_prefix"]
    ind_period = config["ind_period"]
    bands_period = config["bands_period"]
    std_bands = config["std_bands"]
    indicator_name = config["indicator_name"]
    sequence_min_len = config["sequence_min_len"]
    sequence_max_len = config["sequence_max_len"]
    plot_indicator = config["plot_indicator"]
    save_calculations = config["save_calculations"]
    float_precision = config["float_precision"]
    csv_separator = config["csv_separator"]



    df = read_csv(file_path=input_folder + file_name, columns_to_take=columns_to_take)

    ind_df, vis_df = calc_indicator(data=df,
                                       ind_value_col=indicator_name,
                                       ind_period=ind_period,
                                       bands_period=bands_period,
                                       std_bands=std_bands)

    if save_calculations:
        fname = f'{output_folder}{calculations_file_name_prefix}_{indicator_name}_{file_name}'
        print(f'Writing file {fname}')
        ind_df.to_csv(fname, float_format=f'%.{float_precision}f', sep=csv_separator)

    probability_df = process_sequences(inp_df=ind_df,
                                       sequence_min_len=sequence_min_len,
                                       sequence_max_len=sequence_max_len,
                                       ind_period=ind_period,
                                       bands_period=bands_period)

    fname = f'{output_folder}{out_file_name_prefix}_{indicator_name}_{file_name}'
    probability_df.to_csv(fname, float_format=f'%.{float_precision}f', sep=csv_separator)
    print(f'Writing file {fname}')

    if plot_indicator:
        print("Plotting indicator...")
        #plt.figure()
        vis_df.plot()
        plt.show()
        print('Close plot and press enter to end.')
        a = sys.stdin.readline()

