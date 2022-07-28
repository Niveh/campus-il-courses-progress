
class BankAccount:
    def __init__(self) -> None:
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balace -= amount

    def print_balance(self):
        print(f"Current balance is: {self.balance}")

    def func(self):
        print(self)


def main():
    customer1 = BankAccount()
    customer1.deposit(400)
    customer1.print_balance()
    customer2 = BankAccount()
    customer2.deposit(20)
    customer2.print_balance()

    customer1.func()


if __name__ == "__main__":
    main()
