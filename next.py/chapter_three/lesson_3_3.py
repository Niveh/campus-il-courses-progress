
class FactorialArgumentError(Exception):
    def __init__(self, arg) -> None:
        self._arg = arg

    def __str__(self):
        return (f"Provided argument {self._arg} is not a positive integer.")

    def get_arg(self):
        return self._arg


def factorial(n):
    try:
        if not isinstance(n, int) or n < 0:
            raise FactorialArgumentError(n)

    except FactorialArgumentError as e:
        print(
            f"Function expected positive integer, instead got {e.get_arg()}")

    else:
        fact = 1
        for i in range(n, 0, -1):
            fact *= i

        return fact


def main():
    print(factorial(4))
    print(factorial(-4))


if __name__ == "__main__":
    main()
