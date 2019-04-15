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

        while True:#count < 1000:
            print(f"Writing message {count}")
            # convert to bytes
            byte_content = win32file.ReadFile(pipe, 64*1024)[1]
            str_content = byte_content.decode( "utf-8" )
            json_content = json.loads(str_content)

            print( f"Read content: {byte_content}" )
            print( f"Read content: {json_content}" )

            some_data = str.encode( f"{count % 4},1.{count},1.{count-1},1.{count+1},1,1544543200," )

            print( f"Writing data to pipe.")
            win32file.WriteFile(pipe, some_data)
            #win32file.flush()
            #time.sleep(1)
            count += 1

        print("finished now")
    #except:
    #    pipe.send_error()
    finally:
        win32file.CloseHandle(pipe)


def pipe_client():
    print("pipe client")
    quit = False

    while not quit:
        try:
            handle = win32file.CreateFile(
                r'\\.\pipe\Foo',
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
            if res == 0:
                print(f"SetNamedPipeHandleState return code: {res}")
            while True:
                resp = win32file.ReadFile(handle, 64*1024)
                print(f"message: {resp}")
        except pywintypes.error as e:
            if e.args[0] == 2:
                print("no pipe, trying again in a sec")
                time.sleep(1)
            elif e.args[0] == 109:
                print("broken pipe, bye bye")
                quit = True


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