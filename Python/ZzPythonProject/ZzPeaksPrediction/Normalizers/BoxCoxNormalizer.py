#http://www.machinelearning.ru/wiki/index.php?title=%D0%9C%D0%B5%D1%82%D0%BE%D0%B4_%D0%91%D0%BE%D0%BA%D1%81%D0%B0-%D0%9A%D0%BE%D0%BA%D1%81%D0%B0
#https://notebooks.azure.com/Yuriy/libraries/data-analysis-applications/html/Coursemate_003_course5_hometask1_timeseries_analysis.ipynb

import pandas as pd
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
import warnings
import numpy as np

from Common.ModelParameters import ModelParameters


def invboxcox(y,lmbda):
   if lmbda == 0:
      return(np.exp(y))
   else:
      return(np.exp(np.log(lmbda*y+1)/lmbda))

params = ModelParameters

quotes = pd.read_csv(params.io_input_data_file, index_col=['Timestamp'])
#wage['daily'] = wage.WAG_C_M*1.0 / wage.index.days_in_month
#quotes.head()

plt.figure(figsize=(15, 7))
quotes.Value.plot()
#wage.daily.plot()
plt.ylabel('Values')
plt.show()

plt.figure(figsize=(15, 10))
seasonal_dcs = sm.tsa.seasonal_decompose(quotes.Value)

seasonal_dcs.plot()
plt.ylabel('Values')
#print("Критерий Дики-Фуллера: p=%f" % sm.tsa.stattools.adfuller(quotes.Value)[1])
plt.show()

print("end")
