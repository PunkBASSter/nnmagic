# Several trading bots and utility scripts in Python integrated with MetaTrader 5#
Note: this was developed before MetaTrader 5 got the official Python interop support
Most of the projects are obsolete since 2019

### Python-MetaTrader integration via named pipes ###
MT Side: MQL4/Experts/PunkBASSter/Mt4BotApi/Mt4BotApi.mq4 - a standard MT expert advisor handling new data events in MT resending it to the Python code and listening for the orders to send.
Python side example: Python/ZzPythonProject/Integration/SingleOrderBotNnZz.py
The named pipe is initialized on the Python side so the correct launching order would be:
1. Launch Python script (e.g. SingleOrderBotNnZz.py).
2. Launch MetaTrader.
3. Make sure the pipe name is the same on both sides in the settings.
4. Launch MT expert advisor.
5. ???
6. Profit.

In MT StrategyTester this setup works fine only with single thread.

### Some hypothesis testing related to ZigZag-based thrading algorithms with LSTM-based ML ###
/Python/ZzPythonProject/
