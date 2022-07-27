from functools import reduce


def double_letter(my_str):
    return "".join(list(map(lambda x: x * 2, list(my_str))))


print(double_letter("python"))
print(double_letter("we are the champions!"))
