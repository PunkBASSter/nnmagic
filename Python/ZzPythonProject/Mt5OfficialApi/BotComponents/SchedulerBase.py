import pymt5adapter as mt5
import logging

logger = mt5.get_logger(path_to_logfile='my_mt5_log.log', loglevel=logging.DEBUG, time_utc=True)

mt5_connected = mt5.connected(
            path=r'C:\Users\user\Desktop\MT5\terminal64.exe',
            portable=True,
            server='MetaQuotes-Demo',
            login=1234567,
            password='password1',
            timeout=5000,
            logger=logger,  # default is None
            ensure_trade_enabled=True,  # default is False
            enable_real_trading=False,  # default is False
            raise_on_errors=True,  # default is False
            return_as_dict=False,  # default is False
            return_as_native_python_objects=False,  # default is False
        )

class SchedulerBase:
    mt_instance = None

    def __init__(self, mt5_connected):

        with mt5_connected as conn:
            try:
                mt5.
                num_orders = mt5.history_orders_total("invalid", "arguments")
            except mt5.MT5Error as e:
                print("We modified the API to throw exceptions for all functions.")
                print(f"Error = {e}")
            # change error handling behavior at runtime
            conn.raise_on_errors = False
            try:
                num_orders = mt5.history_orders_total("invalid", "arguments")
            except mt5.MT5Error:
                pass
            else:
                print('We modified the API to silence Exceptions at runtime')


    def register_time_series(self, symbol, tf, start, end):
        return self
