def add(num1, num2):
    print(f"The result is {num1 + num2}")


def main():
    add(3, 1)


if __name__ == "__main__":
    main()
    print("I'm running as a script!")
    print(f"My __name__ is: {__name__}")

else:
    print("I'm imported!")
    print(f"My __name__ is: {__name__}")
