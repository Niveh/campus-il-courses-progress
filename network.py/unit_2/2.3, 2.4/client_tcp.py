import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8820))

data = ""
while data != "Bye":
    msg = input("Type your message: ")
    s.send(msg.encode())
    data = s.recv(1024).decode()
    print(f"The server sent {data}")


print("Closing client socket")
s.close()
