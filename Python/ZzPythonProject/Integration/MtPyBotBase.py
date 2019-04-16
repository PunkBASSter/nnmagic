import json
import pandas as pd
from Integration.Mt5PipeConnector import PipeServer as pipe


class StateStr:
    InitStart = "init_start"
    InitProgress = "init_progress"


class MtPyBotBase:
    """Encapsulates basic API calls and structure of MT bot business logic"""
    """Response format; Traded assets; Pipe management mb; """

    _data: pd.DataFrame
    _state: str

    def __init__(self):
        self._data = None
        self._state = "init"

    def process_json_data(self, data_updates: str) -> str:

        json_dict = json.loads(data_updates)
        temp_df = pd.DataFrame(json_dict["data"])
        #temp_df.reset_index()
        temp_df = temp_df.set_index("timestamp")
        #temp_df_t = pd.DataFrame(json_dict["data"]).transpose()
        if self._data is None:
            self._data = temp_df
        else:
            df = pd.concat([self._data, temp_df]) #  (MERGE)
            self._data = df[~df.index.duplicated(keep='last')]

        if temp_df.__len__() == 1:
            self._data = self._data[~self._data.index.duplicated(keep='last')]
            #init finished?
            print("END!")

        return "result"


if __name__ == '__main__':

    bot = MtPyBotBase()

    pipe.pipe_server(bot.process_json_data)