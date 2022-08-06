import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 8820))
s.listen()
print("Server is up and running")


client_socket, client_address = s.accept()
print("Client Connected")
data = ""
while data != "Quit":
    data = client_socket.recv(1024).decode()
    print("Client sent: " + data)
    if data == "Bye":
        data = ""

    elif data == "Quit":
        print("Closing client socket...")
        client_socket.send("Bye".encode())
        break

    client_socket.send(f"{data.upper()}!!!".encode())


client_socket.close()
s.close()
