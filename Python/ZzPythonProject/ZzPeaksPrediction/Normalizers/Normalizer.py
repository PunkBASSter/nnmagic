import pandas as pd


class Normalizer:
    """Input sequences must be sorted by timestamp ascending"""
    _params = None

    def __init__(self, params):
        self._params = params

class Parameters:
    input_file_path = "C:\\Users\\PunkBASSter\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\DzzExportEURUSD.mPERIOD_H1.csv"
    normalized_file_path = "C:\\Users\\PunkBASSter\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\Normalized_DzzExportEURUSD.mPERIOD_H1.csv"
    predicted_file_path = "C:\\Users\\PunkBASSter\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\Predicted_DzzExportEURUSD.mPERIOD_H1.csv"

