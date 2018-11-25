import Integration.PyWPipe as pipe


pserver: pipe.Server
try:
    pserver = pipe.Server( pipe.get_pipe_path('pipe') )

finally:
    pserver.close()