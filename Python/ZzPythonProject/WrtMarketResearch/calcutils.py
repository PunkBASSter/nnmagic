import pandas as pd
import math
import numpy as np
from scipy.signal import argrelextrema

indicator = None

def calc_indicator(df: pd.DataFrame, indicator_func, ind_period: int = 1) -> pd.DataFrame:
    #df['date'] = df.timestamp.apply(datetime.datetime.fromtimestamp)
    df[indicator] = indicator_func(df).rolling(ind_period).mean()
    return df


def get_bands_col_names(std_bands: []) -> []:
    return [f'Std_{k}' for k in std_bands]


def calc_bands(df: pd.DataFrame, std_bands: [], bands_period: int) -> pd.DataFrame:
    df['ma'] = df[indicator].rolling( bands_period ).mean()
    df['std'] = df[indicator].rolling( bands_period ).std()

    for k in std_bands:
        df[f'Std_{k}'] = df['ma'] + df['std'].multiply( k )
    std_band_cols = get_bands_col_names(std_bands)  # Bands column headers

    ind_with_bands = pd.DataFrame(df[[indicator] + std_band_cols], index=df.index)
    return ind_with_bands


def _find_local_extrema(df: pd.DataFrame, order: int = 1) -> pd.DataFrame:
    temp_df = pd.DataFrame( df[[indicator]], index=df.index )
    temp_df['min'] = temp_df.iloc[argrelextrema(temp_df[indicator].values, np.less_equal, order=order)[0]][indicator]
    temp_df['max'] = temp_df.iloc[argrelextrema(temp_df[indicator].values, np.greater_equal, order=order)[0]][indicator]
    return temp_df


def calc_zigzag(df: pd.DataFrame, extr_order: int) -> pd.Series:
    extr_df = _find_local_extrema(df, extr_order)
    last_min_i, last_max_i = -1, -1
    extr_df["zigzag"] = math.nan
    mins, maxs, zz = extr_df["min"], extr_df["max"], extr_df["zigzag"]
    for i in range( 0, extr_df.__len__() ):
        if last_min_i >= last_max_i:
            if not math.isnan( mins[i] ):
                zz[last_min_i] = math.nan
                zz[i] = mins[i]
                last_min_i = i
            if not math.isnan( maxs[i] ):
                zz[i] = maxs[i]
                last_max_i = i
        if last_max_i >= last_min_i:
            if not math.isnan( maxs[i] ):
                zz[last_max_i] = math.nan
                zz[i] = maxs[i]
                last_max_i = i
            if not math.isnan( mins[i] ):
                zz[i] = mins[i]
                last_min_i = i
    return zz


def calc_zz_pattern(df: pd.DataFrame) -> pd.Series:
    def _calc_zz_pattern(a, b, c, d):
        if c <= a and d < b and d < a and b < a: return 0
        if c <= a and d >= b and d < a and b < a: return 1
        if c > a and d >= b and d <= a and b < a: return 2
        if c > a and d < b and d < a and b < a: return 3
        if c > a and d > b and d > a and b < a: return 4
        if c < a and d < b and d < a and b > a: return 5
        if c > a and d <= b and d > a and b > a: return 6
        if c < a and d <= b and d >= a and b > a: return 7
        if c < a and d > b and d > a and b > a: return 8
        if c > a and d > b and d > a and b > a: return 9
        return -1

    zz = df.zigzag[df.zigzag > 0]
    pat_df = pd.DataFrame( zz )
    pat_df["a"] = zz.shift( 3 )
    pat_df["b"] = zz.shift( 2 )
    pat_df["c"] = zz.shift( 1 )
    pat_df["d"] = zz
    pat_df["pattern"] = pat_df.apply(lambda row: _calc_zz_pattern(row["a"], row["b"], row["c"], row["d"]),axis=1)
    return pat_df["pattern"]


def calc_zz_ray_len(df: pd.DataFrame) -> pd.Series:
    zz = df.zigzag[df.zigzag > 0]
    return pd.Series(zz.index, index=zz.index).diff()


def get_bollinger_zone(df: pd.DataFrame, std_bands: []) -> pd.Series:
    def _determine_zone(std_cell_list: [], indicator_calculated_value_column):
        bands_total = std_cell_list.__len__()
        for i in range( 0, bands_total ):
            if indicator_calculated_value_column <= std_cell_list[i]:
                return i + 1
        return bands_total + 1 if not math.isnan( std_cell_list[bands_total - 1] ) else math.nan

    std_band_cols = get_bands_col_names(std_bands)
    return df.apply(lambda row: _determine_zone([row[ki] for ki in std_band_cols], row[indicator]), axis=1)


def get_bollinger_direction(df: pd.DataFrame, std0_col: str = "Std_0") -> pd.Series:
    tmp = df[std0_col].diff()

    def _get_dir(val):
        if val > 0: return 1
        if val < 0: return -1
        if math.isnan(val): return math.nan
        return 0

    return tmp.apply(lambda row: _get_dir(row))


def get_bands_range(df: pd.DataFrame, std_bands: []) -> pd.Series:
    band_cols = get_bands_col_names(std_bands)
    upper_band = band_cols[-1]
    lower_band = band_cols[0]
    return df[upper_band] - df[lower_band]


def get_hl_atr_diff(df: pd.DataFrame, atr_period: int = 30) -> pd.Series:
    rng = df.high - df.low
    atr = rng.rolling(atr_period).mean()
    return rng - atr
