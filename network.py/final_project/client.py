import socket
import chatlib
from question import Question

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS


def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message. 
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    msg = chatlib.build_message(code, data)
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
    return cmd, data


def build_send_recv_parse(conn, cmd, data):
    build_and_send_message(conn, cmd, data)
    msg_code, data = recv_message_and_parse(conn)

    return msg_code, data


def get_score(conn):
    msg_code, data = build_send_recv_parse(
        conn, chatlib.PROTOCOL_CLIENT["score_msg"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["score_msg"]:
        print(f"Your score is {data}")

    else:
        print("Error getting score")


def get_highscore(conn):
    msg_code, data = build_send_recv_parse(
        conn, chatlib.PROTOCOL_CLIENT["highscore_msg"], "")

    if msg_code == chatlib.PROTOCOL_SERVER["highscore_msg"]:
        print(f"High-Score table:\n{data}")

    else:
        print("Error getting highscores")


def check_answer(conn, qid, answer):
    msg_code, data = build_send_recv_parse(
        conn, chatlib.PROTOCOL_CLIENT["answer_msg"], f"{qid}#{answer}")

    if msg_code == chatlib.PROTOCOL_SERVER["correct_answer_msg"]:
        print("Correct answer!")

    elif msg_code == chatlib.PROTOCOL_SERVER["wrong_answer_msg"]:
        print(f"Nope, the correct answer is #{data}")

    elif msg_code == chatlib.PROTOCOL_SERVER["error_msg"]:
        print("A connection error occured.")

    else:
        print("ERROR")


def parse_question(q):
    q = q.split("#")
    question = Question(q[0], q[1], q[2:])
    return question


def play_question(conn):
    msg_code, data = build_send_recv_parse(
        conn, chatlib.PROTOCOL_CLIENT["question_msg"], "")

    if msg_code == chatlib.PROTOCOL_SERVER["question_msg"]:
        question = parse_question(data)
        print(question)
        answer = input("Please choose an answer [1-4]: ")
        check_answer(conn, question.get_id(), answer)

    elif msg_code == chatlib.PROTOCOL_SERVER["gameover_msg"]:
        print("Game Over! We ran out of questions.")


def get_logged_users(conn):
    msg_code, data = build_send_recv_parse(
        conn, chatlib.PROTOCOL_CLIENT["logged_users_msg"], "")

    if msg_code == chatlib.PROTOCOL_SERVER["logged_users_msg"]:
        print(data)

    elif msg_code == chatlib.PROTOCOL_SERVER["error_msg"]:
        print("Error getting logged users")


def connect():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((SERVER_IP, SERVER_PORT))
    return conn


def error_and_exit(error_msg):
    print(error_msg)
    exit()


def login(conn):
    logged_in = False
    while not logged_in:
        username = input("Please enter username: ")
        password = input("Please enter password: ")

        build_and_send_message(
            conn, chatlib.PROTOCOL_CLIENT["login_msg"], f"{username}#{password}")

        login_cmd, login_msg = recv_message_and_parse(
            conn)

        logged_in = login_cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]

        if not logged_in:
            if login_cmd == chatlib.PROTOCOL_SERVER["error_msg"]:
                print(login_msg)

    print("Successfully logged in!")


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    print("Goodbye!")


def show_menu_and_get_action():
    print("p\tPlay a trivia question")
    print("s\tGet my score")
    print("h\tGet high score")
    print("l\tGet logged users")
    print("q\tQuit")
    return input("Please enter your choice: ").strip().lower()


def main():
    conn = connect()
    login(conn)

    while True:
        action = show_menu_and_get_action()
        if action == "q":
            break

        if action == "p":
            play_question(conn)
        elif action == "s":
            get_score(conn)
        elif action == "h":
            get_highscore(conn)
        elif action == "l":
            get_logged_users(conn)

    logout(conn)


if __name__ == '__main__':
    main()
