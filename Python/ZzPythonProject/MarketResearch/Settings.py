import json

class Settings():
    path = 'C:\\Users\\PunkBASSter\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\'
    file_name = 'Rates_EURUSD_PERIOD_H1.csv'
    ind_period = 1  # Indicator mean period
    bands_period = 20  # Base MA period for Bands
    std_bands = [-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5]  # STD multipliers for bands
    ind_value_col = 'body'  # Indicator Value column name
    sequence_min_len = 3
    sequence_max_len = 5  # Length of sequences of Indicator Values to analyse

settings = Settings()
s = json.dumps(settings, default=lambda x: x.__dict__)

print('!')