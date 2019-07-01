import pandas as pd


class SymbolPeriodTimeContainer:
    """Container using indexing as tuples of (<Symbol>,<Period(Time Frame)>,<Timestamp>)."""
    _symbol_tfs_dfs = {}

    def init_keys(self, keys: {}):
        """Consumes a dictionary where key is a Symbol name and value is a list of int timeframes"""
        for cmposite_key in keys:
            self._symbol_tfs_dfs[cmposite_key.key] = dict.fromkeys(cmposite_key.value, pd.DataFrame())

    def add_values_with_key_check(self, symbol: str, period: int, timestamp_df: pd.DataFrame) -> None:
        if symbol in self._symbol_tfs_dfs:
            if period in self._symbol_tfs_dfs[symbol]:
                self._symbol_tfs_dfs[symbol][period]=timestamp_df.combine_first(self._symbol_tfs_dfs[symbol][period])
            else:
                self._symbol_tfs_dfs[symbol][period]=timestamp_df
        else:
            self._symbol_tfs_dfs[symbol]={}
            self._symbol_tfs_dfs[symbol][period] = timestamp_df

    def add_values_by_existing_key(self, symbol: str, period: int, timestamp_df: pd.DataFrame) -> int:
        """timestamp_df MUST have index column 'timestamp'. Supposed to be used for realtime updates(on_tick)."""
        df = self._symbol_tfs_dfs[symbol][period]
        prev_len = df.__len__()
        self._symbol_tfs_dfs[symbol][period]=timestamp_df.combine_first(df)
        return prev_len - self._symbol_tfs_dfs[symbol][period].__len__()

    def get_values(self, symbol: str, period: int) -> pd.DataFrame:
        return self._symbol_tfs_dfs[symbol][period]

    def get_last_values(self, symbol: str, period: int, number: int) -> pd.DataFrame:
        return self.get_values(symbol, period).tail(number)

    def get_values_since(self, symbol: str, period: int, timestamp: int) -> pd.DataFrame:
        return self._symbol_tfs_dfs[symbol][period].loc[timestamp:]

    def extend_data(self, symbol: str, period: int, df_update: pd.DataFrame) -> pd.DataFrame:
        df = self._symbol_tfs_dfs[symbol][period]
        df = df.append(df_update)
        self._symbol_tfs_dfs[symbol][period] = df
        return df

    def __getitem__(self, item):
        return self._symbol_tfs_dfs[item]

    def __setitem__(self, key, value):
        self._symbol_tfs_dfs[key] = value
