import pandas as pd
import matplotlib.pyplot as plt
import math
import datetime
import numpy as np

#Expected Input file format: "timestamp,open,high,low,close,tick_volume,spread,real_volume\n"
#Specify your terminal folder and filename
path = 'C:\\Users\\PunkBASSter\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\'
file_name = 'Rates_EURUSD_PERIOD_H1.csv'

ind_period = 1 #Indicator mean period
bands_period = 20 #Base MA period for Bands
std_bands = [-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5] #STD multipliers for bands
ind_value_col = 'body' #Indicator Value column name
sequence_min_len = 3
sequence_max_len = 8 #Length of sequences of Indicator Values to analyse

print('Filling DataFrame with basic data, Indicator Values, MA, STD')
columns_to_take = ['timestamp', 'open', 'close']
data = pd.read_csv(path+file_name)[columns_to_take]
data['date'] = data.timestamp.apply(datetime.datetime.fromtimestamp)
data[ind_value_col] = (data.close - data.open).rolling( ind_period).mean()
data['ma'] = data[ind_value_col].rolling( bands_period ).mean()
data['std'] = data[ind_value_col].rolling( bands_period ).std()

print('Calculating Bands of MA+K*STD')
for k in std_bands:
    data[f'Std_{k}'] = data['ma'] + data['std'].multiply(k)
std_band_cols = [f'Std_{k}' for k in std_bands] #Bands column headers

#Visualizing Indicator
result_df = pd.DataFrame( data[[ind_value_col] + std_band_cols], index=data.index )
#plt.figure()
#result_df.plot()

print('Defining a zone based on bands where Indicator Value is located')
def get_zone(std_cell_list : [], ind_func_res):
    bands_total = std_cell_list.__len__()
    for i in range(0, bands_total):
        if ind_func_res <= std_cell_list[i]:
            return i+1
    return bands_total + 1 if not math.isnan(std_cell_list[bands_total-1]) else math.nan
result_df['zone'] = result_df.apply( lambda row: get_zone( [row[ki] for ki in std_band_cols], row[ind_value_col] ), axis=1 )

print('Processing sequences')

sequence_len = sequence_min_len #todo LOOP
#Extracting Sequences for probability estimation
seq_cols = [str(c) for c in range( sequence_len )]
seq_cols.reverse()
for c in seq_cols:
    result_df[c] = result_df['zone'].shift(int(c))

zones = range(1, len(std_bands)+2)
sequence_df = result_df.loc[ind_period -1 + bands_period-1 + sequence_len - 1:, seq_cols]#.loc[:, ::-1]
plain_df = sequence_df.groupby(seq_cols).size().reset_index(name='count')
plain_df['prob'] = plain_df['count'].div(sequence_df.count())
grouped_df = plain_df.loc[:, seq_cols[:len(seq_cols)-1]].drop_duplicates(keep='first')

for seq in grouped_df:
    print("!")
#sequence_df = sequence_df.groupby(sequence_df.columns.tolist()).size().reset_index(name='count')  #size().div(len_sequence_df)
#sequence_df['probability'] = sequence_df.apply(lambda row: lambda :row['count']/sequence_df.size(), axis=1)
prob_df = sequence_df
print('end')
