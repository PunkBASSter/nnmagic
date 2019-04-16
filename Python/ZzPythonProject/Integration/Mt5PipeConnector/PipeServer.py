import time
import sys
import win32pipe, win32file, pywintypes
import json
from Integration.MtPyBotBase import MtPyBotBase


def pipe_server(process_str_callback):
    print("pipe server")
    count = 0
    pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\MyDataPipe',
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_READMODE_BYTE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)
    try:
        print("Waiting for client...")
        win32pipe.ConnectNamedPipe(pipe, None)
        print("Got client.")

        while True:
            print(f"Reading message #{count}")

            byte_content = win32file.ReadFile(pipe, 64*1024)[1]
            str_content = byte_content.decode("utf-8")

            print(f"Received content: {str_content}. Calling processing_str_callback...")
            processing_result = process_str_callback(str_content)

            #some_data = str.encode( f"{count % 4},1.{count},1.{count-1},1.{count+1},1,1544543200,")

            print(f"Writing data to pipe.")
            win32file.WriteFile(pipe, str.encode(processing_result))
            #win32file.flush()

            #time.sleep(1)
            count += 1


    except:
        pipe.send_error()
    finally:
        win32file.CloseHandle(pipe)


