import time
import sys
import win32pipe, win32file, pywintypes
import json


def pipe_server():
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

            # convert bytes to json
            byte_content = win32file.ReadFile(pipe, 64*1024)[1]
            str_content = byte_content.decode("utf-8")
            json_content = json.loads(str_content)
            print(f"Received content: {str_content}")

            


            some_data = str.encode( f"{count % 4},1.{count},1.{count-1},1.{count+1},1,1544543200,")

            print(f"Writing data to pipe.")
            win32file.WriteFile(pipe, some_data)
            #win32file.flush()
            #time.sleep(1)
            count += 1

        print("finished now")
    #except:
    #    pipe.send_error()
    finally:
        win32file.CloseHandle(pipe)


if __name__ == '__main__':
    #if len(sys.argv) < 2:
    #    print("need s or c as argument")
    #elif sys.argv[1] == "s":
    #    pipe_server()
    #elif sys.argv[1] == "c":
    #    pipe_client()
    #else:
    #    print(f"no can do: {sys.argv[1]}")
    pipe_server()