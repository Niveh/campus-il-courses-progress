import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_ADDR = ("0.0.0.0", 5555)

messages_to_send = []


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


def main():
    print("Setting up server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(SERVER_ADDR)
    s.listen()
    print("Listening for clients...")
    client_sockets = []

    while True:
        ready_to_read, ready_to_write, in_error = select.select(
            [s] + client_sockets, client_sockets, [])

        for current_socket in ready_to_read:
            if current_socket is s:
                conn, addr = current_socket.accept()
                print("New client joined!", addr)
                client_sockets.append(conn)
                # print_client_sockets(client_sockets)
            else:
                print("New data from client!")
                try:
                    data = current_socket.recv(MAX_MSG_LENGTH).decode()
                    if data == "":
                        print("Connection closed!")
                        client_sockets.remove(current_socket)
                        current_socket.close()
                        # print_client_sockets(client_sockets)

                    else:
                        print(data)
                        messages_to_send.append((current_socket, data))

                except:
                    client_sockets.remove(current_socket)
                    current_socket.close()
                    print("Removed bad socket")
                    print_client_sockets(client_sockets)

        for message in messages_to_send:
            current_socket, data = message
            if current_socket in ready_to_write:
                current_socket.send(data.encode())
                messages_to_send.remove(message)


if __name__ == "__main__":
    main()
