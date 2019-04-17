import json
import pandas as pd
import Mt5PipeConnector.PipeServer as pipe

STATE_INIT = "INIT"
STATE_TICK = "TICK"
SUCCESS_RESULT = "OK"
ERROR_RESULT = "ERROR"


class OrderDto:
    Action: str
    OpenPrice: float
    StopLoss: float
    TakeProfit: float


class MtPyBotBase:
    """Encapsulates basic API calls and structure of MT bot business logic"""
    """Response format; Traded assets; Pipe management mb; """

    _response_format: str
    _data: pd.DataFrame
    _state: str

    def __init__(self, response_format=""):
        self._data = pd.DataFrame()
        self._state = "INIT"
        self._response_format = response_format

    def process_json_data(self, data_updates: str) -> str:

        json_dict = json.loads(data_updates)
        self._state = json_dict["state"]

        if self._state == STATE_INIT:
            try:
                temp_df = pd.DataFrame(json_dict["data"])
                temp_df = temp_df.set_index("timestamp")
                self._data = pd.concat([self._data, temp_df])
                return SUCCESS_RESULT
            except Exception as e:
                return ERROR_RESULT + "_" + e.__str__()

        if self._state == STATE_TICK:
            self._data = self._data[~self._data.index.duplicated(keep='last')]
            result = self.on_tick_handler()
            return result

        return ERROR_RESULT

    def on_tick_handler(self) -> str:
        return self._on_tick_internal()

    def _on_tick_internal(self):
        return SUCCESS_RESULT


if __name__ == '__main__':

    bot = MtPyBotBase()

    pipe.pipe_server(bot.process_json_data)