import socket
import time
import random

SERVER_NAME = "Basic Commands Server"
SERVER_ADDR = ("0.0.0.0", 999)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(SERVER_ADDR)
s.listen(1)

client, addr = s.accept()


def send_message(client, msg):
    client.send(msg.encode())


def recv_message(client):
    return client.recv(1024).decode()


while True:
    data = recv_message(client)
    if data == "Quit":
        send_message("Bye!")
        break

    if data == "NAME":
        send_message(client, f'Server name is: {SERVER_NAME}')
    elif data == "TIME":
        send_message(client, f'Current time: {time.ctime()}')
    elif data == "RAND":
        send_message(client,
                     f'Random number (1-10) is: {random.randint(1, 10)}')

client.close()
s.close()
