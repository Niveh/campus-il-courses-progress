##############################################################################
# server.py
##############################################################################

import socket
import chatlib

# GLOBALS
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    msg = chatlib.build_message(code, data)
    print("[SERVER]", msg)
    conn.send(msg.encode())


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    full_msg = conn.recv(chatlib.MAX_DATA_LENGTH).decode()
    cmd, data = chatlib.parse_message(full_msg)
    print("[CLIENT]", full_msg)
    return cmd, data


# Data Loaders #

def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    questions = {
        2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        4122: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpellier"], "correct": 3}
    }

    return questions


def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """
    users = {
        "test":	{"password": "test", "score": 0, "questions_asked": []},
        "yossi":	{"password": "123", "score": 50, "questions_asked": []},
        "master":	{"password": "master", "score": 200, "questions_asked": []}
    }
    return users


# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen()

    return sock


def send_error(conn, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    build_and_send_message(
        conn, chatlib.PROTOCOL_SERVER["error_msg"], error_msg)


# MESSAGE HANDLING


def handle_getscore_message(conn, username):
    global users
    # Implement this in later chapters


def handle_logout_message(conn):
    """
    Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
    Recieves: socket
    Returns: None
    """
    global logged_users
    conn.close()


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users	 # To be used later

    username, password = data.split("#")
    if username in users:
        if users[username]["password"] == password:
            build_and_send_message(
                conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
        else:
            send_error(conn, "Incorrect password!")
    else:
        send_error(conn, "Username does not exist!")


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users	 # To be used later

    if cmd == chatlib.PROTOCOL_CLIENT["login_msg"]:
        handle_login_message(conn, data)
    elif cmd == chatlib.PROTOCOL_CLIENT["logout_msg"]:
        handle_logout_message(conn)
    else:
        send_error(conn, "Unknown command")


def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global questions

    print("Welcome to Trivia Server!")
    users = load_user_database()
    questions = load_questions()
    s = setup_socket()

    while True:
        print("Waiting for new connection...")
        conn, addr = s.accept()
        print(f"Incoming connection: {addr}")
        try:
            while conn.fileno() != -1:
                cmd, data = recv_message_and_parse(conn)

                if (cmd, data) == (None, None):
                    conn.close()
                    raise Exception

                handle_client_message(conn, cmd, data)
        except:
            print(f"Lost connection with {addr}")

        else:
            print(f"Client logged out from {addr}")


if __name__ == '__main__':
    main()
