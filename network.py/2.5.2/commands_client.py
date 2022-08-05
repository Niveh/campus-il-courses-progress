import socket

SERVER_ADDR = ("127.0.0.1", 999)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDR)

data = ""
while data != "Quit":
    msg = input("Enter a command: ")
    s.send(msg.encode())
    data = s.recv(1024).decode()
    print(data)

s.close()
