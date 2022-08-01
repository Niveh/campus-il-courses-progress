def square(num):
    return num ** 2


def factorial(n):
    fact = 1
    for i in range(n, 0, -1):
        fact = fact * i
    return fact


def is_prime(n):
    if n <= 1:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False

    return True
