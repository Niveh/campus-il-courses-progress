import socket

SERVER_ADDR = ("127.0.0.1", 5555)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDR)

while True:
    pass

s.close()
