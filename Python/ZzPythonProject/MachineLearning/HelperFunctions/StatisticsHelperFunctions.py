#http://www.machinelearning.ru/wiki/index.php?title=%D0%9C%D0%B5%D1%82%D0%BE%D0%B4_%D0%91%D0%BE%D0%BA%D1%81%D0%B0-%D0%9A%D0%BE%D0%BA%D1%81%D0%B0
#https://notebooks.azure.com/Yuriy/libraries/data-analysis-applications/html/Coursemate_003_course5_hometask1_timeseries_analysis.ipynb
from scipy import stats
import statsmodels.api as sm


def shift_to_positive(buff):
    min = buff.min()

    if min < 0:
        shift = abs(min)
        return buff + shift, shift
    return buff, 0


def is_stationary(collection):
    test = sm.tsa.stattools.adfuller(collection)
    if test[0] > test[4]['5%']:
        print("NOT stationary.")
        return False
    print("Stationary.")
    return True


def is_normal(collection, alpha=1e-3):
    k2, p = stats.normaltest(collection)
    print("p = {:g}".format(p))
    if p < alpha:
        print("NOT Normal")
        return False
    print("May be Normal")
    return True

