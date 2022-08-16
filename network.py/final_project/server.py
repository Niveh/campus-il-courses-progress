##############################################################################
# server.py
##############################################################################

import socket
import chatlib
import random
import json
import requests
import html

# GLOBALS
users = {}
questions = {}
logged_users = {}
waiting_for_answer = {}

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"

USERS_FILE = "users.txt"
QUESTIONS_FILE = "questions.txt"

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
def fix_data(data):
    return html.unescape(data).replace("#", "__HASH__")


def load_questions_from_web():
    global questions

    # r = requests.get("https://opentdb.com/api.php?amount=50&type=multiple")
    r = requests.get(
        "https://opentdb.com/api.php?amount=50&category=18&type=multiple")

    results = json.loads(r.text)["results"]

    for i, q in enumerate(results):
        question_id = i + 1

        question = fix_data(q["question"])
        correct_answer = fix_data(
            q["correct_answer"])

        incorrect_answers = q["incorrect_answers"]
        incorrect_answers = list(map(fix_data, incorrect_answers))

        answers = [correct_answer] + incorrect_answers

        random.shuffle(answers)

        questions[str(question_id)] = {
            "question": question,
            "answers": answers,
            "correct": answers.index(correct_answer) + 1
        }


def load_questions():
    """
    Loads questions bank from file
    Recieves: -
    Returns: questions dictionary
    """
    with open(QUESTIONS_FILE, "r") as f:
        data = f.read()
        return json.loads(data)


def load_user_database():
    """
    Loads users list from file
    Recieves: -
    Returns: user dictionary
    """
    with open(USERS_FILE, "r") as f:
        data = f.read()
        return json.loads(data)


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


def create_random_question(username):
    global questions
    global users
    user_questions = users[username]["questions_asked"]
    question_ids = [qid for qid in questions.keys()]

    available_questions = list(filter(
        lambda x: x not in user_questions, question_ids))

    if len(available_questions) == 0:
        return None

    random_question_id = random.choice(available_questions)

    users[username]["questions_asked"] = user_questions + [random_question_id]

    question = questions[random_question_id]["question"]
    answers = questions[random_question_id]["answers"]

    return f"{random_question_id}#{question}#{'#'.join(answers)}"

# MESSAGE HANDLING


def handle_question_message(conn):
    username = logged_users[conn.getpeername()]
    question = create_random_question(username)
    if question:
        global waiting_for_answer
        waiting_for_answer[username] = question.split("#")[0]
        build_and_send_message(
            conn, chatlib.PROTOCOL_SERVER["question_msg"], question)
    else:
        build_and_send_message(
            conn, chatlib.PROTOCOL_SERVER["gameover_msg"], "")


def handle_answer_message(conn, username, data):
    global waiting_for_answer
    question_id, answer = data.split("#")

    if username not in waiting_for_answer:
        build_and_send_message(
            conn, chatlib.PROTOCOL_SERVER["error_msg"], "")
        return

    if question_id not in waiting_for_answer[username]:
        build_and_send_message(
            conn, chatlib.PROTOCOL_SERVER["error_msg"], "")
        return

    correct = questions[question_id]["correct"]

    if int(answer) == correct:
        users[username]["score"] += 5
        build_and_send_message(
            conn, chatlib.PROTOCOL_SERVER["correct_answer_msg"], "")
    else:
        build_and_send_message(
            conn, chatlib.PROTOCOL_SERVER["wrong_answer_msg"], str(correct))

    waiting_for_answer[username] = ""


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
    logged_users.pop(conn.getpeername(), None)
    conn.close()


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users
    global logged_users

    username, password = data.split("#")
    if username in logged_users:
        build_and_send_message(
            conn, chatlib.PROTOCOL_SERVER["error_msg"], "You are already logged in!")
        return

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
    global logged_users

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
    global questions

    print("Welcome to Trivia Server!")
    users = load_user_database()
    load_questions_from_web()

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
        except Exception as e:
            print(e)
            print(f"Lost connection with {addr}")

        else:
            print(f"Client logged out from {addr}")


if __name__ == '__main__':
    main()
