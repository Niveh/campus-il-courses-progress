import string


class LoginException(Exception):
    def __init__(self) -> None:
        super().__init__()


class UsernameContainsIllegalCharacter(LoginException):
    def __init__(self, char, index) -> None:
        super().__init__()
        self._char = char
        self._index = index

    def __str__(self):
        return f'The username contains an illegal character "{self._char}" at index {self._index} '


class UsernameTooShort(LoginException):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return "The username is too short"


class UsernameTooLong(LoginException):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return "The username is too long"


class PasswordMissingCharacter(LoginException):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return "The password is missing a character"


class PasswordMissingCharacterUppercase(PasswordMissingCharacter):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return super().__str__() + " (Uppercase)"


class PasswordMissingCharacterLowercase(PasswordMissingCharacter):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return super().__str__() + " (Lowercase)"


class PasswordMissingCharacterDigit(PasswordMissingCharacter):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return super().__str__() + " (Digit)"


class PasswordMissingCharacterSpecial(PasswordMissingCharacter):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return super().__str__() + " (Special)"


class PasswordTooShort(LoginException):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return "The password is too short"


class PasswordTooLong(LoginException):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return "The password is too long"


def check_input(username, password):
    try:
        for char in username:
            if not (char.isalpha() or char.isnumeric() or char == "_"):
                raise UsernameContainsIllegalCharacter(
                    char, username.index(char))

        if len(username) < 3:
            raise UsernameTooShort

        elif len(username) > 16:
            raise UsernameTooLong

        elif len(password) < 8:
            raise PasswordTooShort

        elif len(password) > 40:
            raise PasswordTooLong

        has_upper = False
        has_lower = False
        has_number = False
        has_symbol = False

        for char in password:
            if char.isalpha():
                if char.isupper():
                    has_upper = True
                elif char.islower():
                    has_lower = True

            elif char.isnumeric():
                has_number = True

            elif char in string.punctuation:
                has_symbol = True

        if not has_upper:
            raise PasswordMissingCharacterUppercase

        elif not has_lower:
            raise PasswordMissingCharacterLowercase

        elif not has_number:
            raise PasswordMissingCharacterDigit

        elif not has_symbol:
            raise PasswordMissingCharacterSpecial

    except LoginException as e:
        print(e)

    else:
        print("OK")
        return True


def main():
    check_input("1", "2")
    check_input("0123456789ABCDEFG", "2")
    check_input("A_a1.", "12345678")
    check_input("A_1", "2")
    check_input("A_1", "ThisIsAQuiteLongPasswordAndHonestlyUnnecessary")
    check_input("A_1", "abcdefghijklmnop")
    check_input("A_1", "ABCDEFGHIJLKMNOP")
    check_input("A_1", "ABCDEFGhijklmnop")
    check_input("A_1", "4BCD3F6h1jk1mn0p")
    check_input("A_1", "4BCD3F6.1jk1mn0p")


if __name__ == "__main__":
    main()
