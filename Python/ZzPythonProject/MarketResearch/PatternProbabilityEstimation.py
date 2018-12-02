import pandas as pd
import matplotlib.pyplot as plt
import math
import datetime
import numpy as np

#header format: "timestamp,open,high,low,close,tick_volume,spread,real_vloume\n"
#Specify your terminal folder
path = 'C:\\Users\\PunkBASSter\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\'
file_name = 'Rates_EURUSD_PERIOD_H4.csv'

bands_period = 20
std_bands = [-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5]
ind_value_col = 'body'

columns_to_take = ['timestamp', 'open', 'close']
data = pd.read_csv(path+file_name)[columns_to_take]
data['date'] = data.apply(lambda row: datetime.datetime.fromtimestamp(row['timestamp']), axis=1)
data[ind_value_col] = data.close - data.open
data['ma'] = data[ind_value_col].rolling( bands_period ).mean()
data['std'] = data[ind_value_col].rolling( bands_period ).std()

for k in std_bands:
    data[str(k)] = data['ma'] + data['std'].multiply(k)

#Bands column headers
k_str = [str(k) for k in std_bands]
result_df = pd.DataFrame( data[[ind_value_col] + k_str], index=data.index )#.loc[bands_period - 1:]
plt.figure()
result_df.plot()

def get_zone(std_cell_list : [], ind_func_res):
    bands_total = std_cell_list.__len__()
    for i in range(0, bands_total):
        if ind_func_res <= std_cell_list[i]:
            return i+1
    return bands_total + 1 if not math.isnan(std_cell_list[bands_total-1]) else math.nan

result_df['zone'] = result_df.apply( lambda row: get_zone( [row[ki] for ki in k_str], row[ind_value_col] ), axis=1 )


print('end')
