import socket

SERVER_ADDR = ("127.0.0.1", 8821)
MAX_MSG_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg = input("Type: ")
    s.sendto(msg.encode(), SERVER_ADDR)
    if msg == "EXIT":
        break

    response, remote_address = s.recvfrom(MAX_MSG_SIZE)
    data = response.decode()
    print(data)

s.close()
