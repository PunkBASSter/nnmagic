#http://www.machinelearning.ru/wiki/index.php?title=%D0%9C%D0%B5%D1%82%D0%BE%D0%B4_%D0%91%D0%BE%D0%BA%D1%81%D0%B0-%D0%9A%D0%BE%D0%BA%D1%81%D0%B0
#https://notebooks.azure.com/Yuriy/libraries/data-analysis-applications/html/Coursemate_003_course5_hometask1_timeseries_analysis.ipynb

import pandas as pd
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
import warnings
import datetime as dt
import numpy as np

from Common.ModelParameters import ModelParameters


def invboxcox(y,lmbda):
   if lmbda == 0:
      return(np.exp(y))
   else:
      return(np.exp(np.log(lmbda*y+1)/lmbda))


def is_stationary(collection):
   test = sm.tsa.stattools.adfuller(collection)
   print('adf: ', test[0])
   print('p-value: ', test[1])
   print('Critical values: ', test[4])
   res = False
   if test[0] > test[4]['5%']:
      print('есть единичные корни, ряд не стационарен')
   else:
      print('единичных корней нет, ряд стационарен')
      res = True
   return res

params = ModelParameters


quotes_df = pd.read_csv(params.io_input_data_file)

quotes_df.reset_index()
quotes_df['Date'] = pd.to_datetime(quotes_df['Timestamp'])
quotes_df.set_index('Date')

#dts = []
#for ts in quotes_df["Timestamp"]:
#   dts.append(dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

#for i in range(0, quotes_df["Timestamp"].__len__()):
#   dts.append(dt.datetime.utcnow().date() + dt.timedelta(days=i))

#quotes_df["FakeDate"] = pd.Series(dts)



#wage['daily'] = wage.WAG_C_M*1.0 / wage.index.days_in_month
#quotes.head()

#plt.figure(figsize=(15, 7))
#quotes_df.Value.plot()
#wage.daily.plot()
#plt.ylabel('Values')
#plt.show()

#plt.figure(figsize=(15, 10))
seasonal_dcs = sm.tsa.seasonal_decompose(quotes_df.Value, freq=500)
#seasonal_dcs.plot()
df = sm.tsa.stattools.adfuller(quotes_df.Value)




#check for stationary - for differences also
is_stationary(quotes_df.Value)
print("\n")

idiff = quotes_df.Value
for i in range(2, 100, 2):
   idiff = quotes_df.Value.diff(periods=i).dropna()
   if is_stationary(idiff):
      print("Autoregression period = "+str(i) + "\n")
      break

quotes_df['ValueBox'], lmbda = stats.boxcox(quotes_df.Value)
plt.figure(figsize=(15, 7))
quotes_df.Value.plot()
quotes_df.ValueBox.plot()
plt.ylabel(u'Transformed values')
print("Оптимальный параметр преобразования Бокса-Кокса: %f" % lmbda)
is_stationary(quotes_df.ValueBox)

idiff.plot()

plt.grid()
#print("Критерий Дики-Фуллера: p=%f" % sm.tsa.stattools.adfuller(quotes.Value)[1])
plt.show()

print("end")
