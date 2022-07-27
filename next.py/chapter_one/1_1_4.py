from functools import reduce


def sum_of_digits(number):
    return reduce(lambda total, n: total + int(n[0]), str(number), 0)


print(sum_of_digits(104))
print(sum_of_digits(111345))
