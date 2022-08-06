import socket

SERVER_ADDR = ("0.0.0.0", 8821)
MAX_MSG_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(SERVER_ADDR)

while True:
    msg, addr = s.recvfrom(MAX_MSG_SIZE)
    data = msg.decode()
    print(f"Client sent: {data}")
    if data == "EXIT":
        break

    response = "Hello " + data
    s.sendto(response.encode(), addr)

s.close()
