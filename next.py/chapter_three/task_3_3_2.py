
class UnderAgeException(Exception):
    def __init__(self, age) -> None:
        self._age = age

    def __str__(self):
        diff = 18 - self._age
        return f"Your age ({self._age}) is too young. Come back in {diff} year{'' if diff == 1 else 's'}."


def send_invitation(name, age):
    try:
        if int(age) < 18:
            raise UnderAgeException(age)

    except UnderAgeException as e:
        print(e)

    else:
        print("You should send an invite to " + name)


def main():
    send_invitation("Older Niv", 20)
    send_invitation("Younger Niv", 17)


if __name__ == "__main__":
    main()
