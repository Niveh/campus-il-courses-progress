from functools import reduce


def is_prime(number):
    return reduce(lambda x, y: x + y, [x for x in range(1, number + 1) if number % x == 0]) == number + 1


print(is_prime(42))
print(is_prime(43))
