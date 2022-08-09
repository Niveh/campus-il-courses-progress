##############################################################################
# server.py
##############################################################################

from calendar import c
import socket
import chatlib
import random
import select

# GLOBALS
users = {}
questions = {}
logged_users = {}
messages_to_send = []

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "0.0.0.0"


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
    global messages_to_send
    messages_to_send.append((conn, msg))


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


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print(c.getpeername())


# Data Loaders #

def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    questions = {
        2313: {"question": "How much is 2+2?", "answers": ["3", "4", "2", "1"], "correct": 2},
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


def create_random_question():
    global questions
    question_id = random.choice([qid for qid in questions.keys()])
    question = questions[question_id]["question"]
    answers = questions[question_id]["answers"]

    return f"{question_id}#{question}#{'#'.join(answers)}"

# MESSAGE HANDLING


def handle_question_message(conn):
    question = create_random_question()
    build_and_send_message(
        conn, chatlib.PROTOCOL_SERVER["question_msg"], question)


def handle_answer_message(conn, username, data):
    question_id, answer = data.split("#")
    correct = questions[int(question_id)]["correct"]

    if int(answer) == correct:
        users[username]["score"] += 5
        build_and_send_message(
            conn, chatlib.PROTOCOL_SERVER["correct_answer_msg"], "")
    else:
        build_and_send_message(
            conn, chatlib.PROTOCOL_SERVER["wrong_answer_msg"], str(correct))


def handle_getscore_message(conn, username):
    global users
    score = str(users[username]["score"])
    build_and_send_message(
        conn, chatlib.PROTOCOL_SERVER["score_msg"], score)


def handle_highscore_message(conn):
    global users

    score_table = [f"{user}: {users[user]['score']}" for user in users]
    scoreboard = "\n".join(
        sorted(score_table, key=lambda x: int(x.split(" ")[1]), reverse=True))

    build_and_send_message(
        conn, chatlib.PROTOCOL_SERVER["highscore_msg"], scoreboard)


def handle_logged_message(conn):
    global logged_users
    user_list = ", ".join([logged_users[user] for user in logged_users])
    build_and_send_message(
        conn, chatlib.PROTOCOL_SERVER["logged_users_msg"], f"Online users: {user_list}")


def handle_logout_message(conn):
    """
    Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
    Recieves: socket
    Returns: None
    """
    global logged_users
    username = logged_users[conn.getpeername()]
    logged_users.pop(conn.getpeername(), None)
    conn.close()
    raise chatlib.LogoutException(username)


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
            logged_users[conn.getpeername()] = username
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
    elif conn.getpeername() not in logged_users:
        return

    elif cmd == chatlib.PROTOCOL_CLIENT["logout_msg"]:
        handle_logout_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["score_msg"]:
        handle_getscore_message(conn, logged_users[conn.getpeername()])
    elif cmd == chatlib.PROTOCOL_CLIENT["highscore_msg"]:
        handle_highscore_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["logged_users_msg"]:
        handle_logged_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["question_msg"]:
        handle_question_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["answer_msg"]:
        handle_answer_message(conn, logged_users[conn.getpeername()], data)
    else:
        send_error(conn, "Unknown command")


def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global logged_users
    global questions
    global messages_to_send

    print("Welcome to Trivia Server!")
    users = load_user_database()
    questions = load_questions()

    s = setup_socket()
    print("Listening for clients...")
    client_sockets = []

    while True:
        ready_to_read, ready_to_write, in_error = select.select(
            [s] + client_sockets, client_sockets, [])

        for current_socket in ready_to_read:
            if current_socket is s:
                conn, addr = current_socket.accept()
                print(f"Incoming connection: {addr}")
                client_sockets.append(conn)
                # print_client_sockets(client_sockets)
            else:
                try:
                    cmd, data = recv_message_and_parse(current_socket)
                    if (cmd, data) == (None, None):
                        raise Exception

                    handle_client_message(current_socket, cmd, data)

                except chatlib.LogoutException as e:
                    print(e)
                    client_sockets.remove(current_socket)

                except Exception as e:
                    print(e)
                    addr = current_socket.getpeername()
                    print(
                        f"Lost connection with {addr}")
                    logged_users.pop(addr, None)
                    client_sockets.remove(current_socket)
                    current_socket.close()

        for message in messages_to_send:
            current_socket, data = message
            if current_socket in ready_to_write:
                current_socket.send(data.encode())
                messages_to_send.remove(message)


if __name__ == '__main__':
    main()
