import math
import pickle
import os.path
import pandas
from SymbolPeriodTimeContainer import SymbolPeriodTimeContainer


class MTxPyDataSource:
    _data_folder: str
    _global_rates_container: SymbolPeriodTimeContainer

    def __init__(self):
        self._data_sources = {}
        self.symbol_periods = None
        self.series_names = ["open", "high", "low", "close"]
        self.empty_value = math.nan
        self._data_container = SymbolPeriodTimeContainer()
        self.is_offline = False

    def calculate(self, symbol: str, period: int, timestamp: int) -> pandas.DataFrame:
        pass

    @property
    def data_container(self) -> SymbolPeriodTimeContainer:
        return self._data_container

    @property
    def indicators(self) -> {}:
        return self._data_sources

    @property
    def data_file_name(self):
        name = f"{type(self).__name__}.mtpy"
        return os.path.join(self._data_folder, name)

    def _save_data(self):
        with open(self.data_file_name, 'wb') as f:
            pickle.dump(self._data_container, f)

    def save_data(self):
        self._save_data()
        for data_source in self._data_sources.values():
            data_source.save_data()

    def _load_data(self):
        self._load_data()
        with open(self.data_file_name, 'rb') as f:
            self._data_container = pickle.load(f)

    def load_data(self):
        for data_source in self._data_sources.values():
            data_source.load_data()
        self._load_data()

    def register_indicator(self, name: str, ind_obj):
        self._data_sources[name] = ind_obj
        return self

    def __getitem__(self, item):
        return self._data_sources[item]

    def _train(self):
        pass

    def train(self):
        self._train()
        for ind in self._data_sources.items():
            ind[1].train()
