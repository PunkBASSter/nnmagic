import win32pipe
import win32file

p = win32pipe.CreateNamedPipe(r'\\.\pipe\test_pipe',
    win32pipe.PIPE_ACCESS_DUPLEX,
    win32pipe.PIPE_TYPE_MESSAGE,
    1, 65536, 65536, 300, None)

p2 = win32pipe.CreateNamedPipe(
    r'\\.\pipe\test_pipe2',
    win32pipe.PIPE_ACCESS_DUPLEX, # open mode
    win32pipe.PIPE_TYPE_MESSAGE, # pipe mode
    1, # max instances
    65536, # out buffer size
    65536, # in buffer size
    0, # timeout
    None)

#connected = win32pipe.ConnectNamedPipe(p2, None);

#win32pipe.ConnectNamedPipe(p, None)

data = "Hello Pipe"
win32file.WriteFile(p2, data)

#---------

fileHandle = win32file.CreateFile("\\\\.\\pipe\\test_pipe",
                              win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                              0, None,
                              win32file.OPEN_EXISTING,
                              0, None)
data = win32file.ReadFile(fileHandle, 4096)
print(data)