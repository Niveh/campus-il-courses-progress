
class BankAccount:
    bank_name = "PayPy"

    def __init__(self, balance=0) -> None:
        self._balance = balance

    def deposit(self, amount):
        self._balance += amount

    def withdraw(self, amount):
        self._balance -= amount

    def print_balance(self):
        print(f"Current balance is {self._balance}")


def main():
    first_account = BankAccount()
    second_account = BankAccount()
    print(first_account.bank_name)
    print(second_account.bank_name)


main()
