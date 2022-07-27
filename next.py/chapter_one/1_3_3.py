from functools import reduce


def is_funny(string):
    return reduce(lambda x, y: x + y, [char for char in string if char == "h" or char == "a"]) == string


print(is_funny("hahahahahaha"))
