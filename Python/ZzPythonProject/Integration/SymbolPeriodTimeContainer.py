import pandas as pd


class SymbolPeriodTimeContainer:
    """Container using indexing as tuples of (<Symbol>,<Period(Time Frame)>,<Timestamp>)."""
    _symbol_tfs_dfs: {}

    def init_keys(self, keys: {}, columns:[]):
        """Consumes a dictionary where key is a Symbol name and value is a list of int timeframes"""
        for cmposite_key in keys:
            self._symbol_tfs_dfs[cmposite_key.key] = dict.fromkeys(cmposite_key.value, pd.DataFrame(columns=columns))

    def add_values(self, symbol: str, tf: int, ts_df: pd.DataFrame) -> None:
        """ts_df MUST have index column 'timestamp'."""
        df = self._symbol_tfs_dfs[symbol][tf]
        ts_df.combine_first(df)
        last_saved = df.tail(1)
        first_update = ts_df.head(1)

