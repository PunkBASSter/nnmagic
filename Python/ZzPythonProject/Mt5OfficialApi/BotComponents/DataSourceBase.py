import math
import pickle
import os.path
import pandas
from SymbolPeriodTimeContainer import SymbolPeriodTimeContainer


class DataSourceBase:
    _data_folder: str
    _global_rates_container: SymbolPeriodTimeContainer

    def __init__(self):
        self._data_sources = {}
        self.symbol_periods = None
        self.series_names = ["open", "high", "low", "close"]
        self.empty_value = math.nan
        self._data_container = SymbolPeriodTimeContainer()
        #self._data_container_offline = SymbolPeriodTimeContainer()
        self.is_offline = False
        self.last_processed = {}

    def calculate(self, symbol: str, period: int, timestamp: int) -> pandas.DataFrame:
        pass

    @property
    def data_container(self) -> SymbolPeriodTimeContainer:
        return self._data_container

    @property
    def indicators(self) -> {}:
        return self._data_sources

    def get_data_file_name(self, add_suffix):
        name = f"{type(self).__name__}_{add_suffix}.mtpy"
        return os.path.join(DataSourceBase._data_folder, name)

    def save_data(self, deep=True, add_suffix=""):
        with open(self.get_data_file_name(add_suffix), 'wb') as f:
            pickle.dump(self._data_container, f)
        if deep:
            for data_source in self._data_sources.values():
                data_source.save_data()

    def load_data(self, deep=True, add_suffix=""):
        if deep:
            for data_source in self._data_sources.values():
                data_source.load_data()
        with open(self.get_data_file_name(add_suffix), 'rb') as f:
            self._data_container_offline = pickle.load(f)

    def register_indicator(self, name: str, ind_obj):
        self._data_sources[name] = ind_obj
        return self

    def __getitem__(self, item):
        return self._data_sources[item]

    def _train(self):
        pass

    def train(self):
        self._train()
        for ind in self._data_sources.values():
            ind.train()
