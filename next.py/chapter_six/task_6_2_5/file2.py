from file1 import GreetingCard


class BirthdayCard(GreetingCard):
    def __init__(self, recipient="Dana Ev", sender="Eyal Ch", sender_age=0) -> None:
        super().__init__(recipient, sender)
        self._sender_age = sender_age

    def greeting_msg(self):
        super().greeting_msg()
        print(f"Happy Birthday! {self._sender_age} is a great age.")
