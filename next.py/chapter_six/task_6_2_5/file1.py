
class GreetingCard:
    def __init__(self, recipient="Dana Ev", sender="Eyal Ch") -> None:
        self._recipient = recipient
        self._sender = sender

    def greeting_msg(self):
        print(f"From: {self._sender}\nTo: {self._recipient}")
