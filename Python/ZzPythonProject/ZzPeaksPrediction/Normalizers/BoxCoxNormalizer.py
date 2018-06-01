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

c = 0.0001

def inv_boxcox(y,lmbda):
   if lmbda == 0:
      return(np.exp(y))
   else:
      return(np.exp(np.log(lmbda*y+1)/lmbda))


def inv_diff(src_first, diff):
    return np.r_[src_first, diff.iloc[1:]].cumsum()


def shift_to_positive(buff):
    min = buff.min()

    if min < 0:
        shift = abs(min)
        return buff + shift, shift
    return buff, 0


def is_stationary(collection):
   test = sm.tsa.stattools.adfuller(collection)
   #print('adf: ', test[0])
   #print('p-value: ', test[1])
   #print('Critical values: ', test[4])
   res = False
   if test[0] > test[4]['5%']:
      print("NOT stationary.") #'есть единичные корни, ряд не стационарен')
   else:
      print("Stationary.") #'единичных корней нет, ряд стационарен')
      res = True
   return res


def is_normal(collection, alpha=1e-3):
    k2, p = stats.normaltest(collection)
    print("p = {:g}".format(p))
    res = True
    if p < alpha:  # null hypothesis: x comes from a normal distribution
        print("NOT normal")
        return False

    print("May be Normal")
    return True

def plot():
    plt.figure(figsize=(15, 7))
    quotes_df.Value.plot()
    shifted_diff, abs_shift = shift_to_positive(quotes_df.ValueDiff)
    (shifted_diff+c).plot()
    quotes_df.DiffBoxCox.plot()

    plt.grid()
    plt.show()

    plt.figure(figsize=(15, 7))
    quotes_df.Value.hist(bins=100)
    (shifted_diff + c).hist(bins=100)
    quotes_df.DiffBoxCox.hist(bins=100)
    plt.grid()
    plt.show()


params = ModelParameters
quotes_df = pd.read_csv(params.io_input_data_file)
#plt.figure(figsize=(15, 7))
#quotes_df.Value.plot()
#wage.daily.plot()
#plt.ylabel('Values')
#plt.show()

#plt.figure(figsize=(15, 10))
#seasonal_dcs = sm.tsa.seasonal_decompose(quotes_df.Value, freq=500)
#seasonal_dcs.plot()

#idiff = quotes_df.Value
#diff_period = 1
#for i in range(1, 100, 1):
#   idiff = quotes_df.Value.diff(periods=i).dropna()
#   diff_period = i
#   if is_stationary(idiff):
#      print("Autoregression period = "+str(i) + "\n")
#      break

quotes_df["ValueBoxCox"], lmbda1 = stats.boxcox(quotes_df["Value"])
quotes_df['ValueDiff'] = quotes_df.Value.diff(periods=1).dropna()

shifted_diff, abs_shift = shift_to_positive(quotes_df.ValueDiff)
shifted_diff=shifted_diff + c
quotes_df['DiffBoxCox'], lmbda = stats.boxcox(shifted_diff)

#plots
plot()

#reverse
quotes_df['DiffInvBoxCox'] = inv_boxcox(quotes_df.DiffBoxCox, lmbda)
unshifted_diff = quotes_df['DiffInvBoxCox'] - abs_shift - c
quotes_df['RestoredDiff'] = inv_diff(quotes_df.Value.iloc[0:1], unshifted_diff)

#is_stationary(quotes_df.Value); is_normal(quotes_df.Value)
is_stationary(quotes_df.ValueBoxCox)
is_normal(quotes_df.ValueBoxCox)
#is_stationary(shifted_diff); is_normal(shifted_diff)
is_stationary(quotes_df.DiffBoxCox)
is_normal(quotes_df.DiffBoxCox)

print("end")
