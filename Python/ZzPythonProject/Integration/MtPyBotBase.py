import json
import pandas as pd

class MtPyBotBase:
    """Encapsulates basic API calls and structure of MT bot business logic"""
    """Response format; Traded assets; Pipe management mb; """

    _data: pd.DataFrame
    _state: str


    def process_json_data(self, data_updates: str) -> str:

        json_dict = json.loads(data_updates)
        temp_df = pd.DataFrame(json_dict["data"])

        if self._data is None:
            self._data = temp_df
        else:
            self._data = self._data #  (MERGE)

        pass

