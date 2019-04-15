import win32pipe, win32file
import ctypes  # An included library with Python install.
import sys
import time

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))


#def mbox(title, text, style):
#    return ctypes.windll.user32.MessageBoxW(0, sys.argv[0], sys.argv[1], style)


#pipeName = sys.argv[1] #str.replace(sys.argv[1], "\\\\", "\\")
pipeName = "\\\\.\\pipe\\PipesOfPiece"

p = win32pipe.CreateNamedPipe(pipeName,
                              win32pipe.PIPE_ACCESS_DUPLEX,
                              win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_WAIT,
                              1, 65536, 65536, 1, None)

#win32pipe.ConnectNamedPipe(p, None)

data = "Hello Pipe"

f = open(pipeName, 'rb')
#f.write(data)


while True:
    try:
        content = f.read()
        time.sleep( 1 )
    finally:
        f.close()

print('Success')

time.sleep(3)

