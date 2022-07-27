from functools import reduce

FILENAME = "names.txt"


def get_longest_name():
    with open(FILENAME, "r") as f:
        return reduce(lambda x, y: x if len(x) > len(y) else y, f.read().split("\n"))


def get_names_length_sum():
    with open(FILENAME, "r") as f:
        return reduce(lambda a, b: a + b, list(map(lambda x: len(x), f.read().split("\n"))))


def get_shortest_names():
    with open(FILENAME, "r") as f:
        names = f.read().split("\n")
        shortest_len = len(
            reduce(lambda x, y: x if len(x) < len(y) else y, names))
        return "\n".join(list(filter(lambda x: len(x) == shortest_len, names)))


def write_name_lengths():
    with open(FILENAME, "r") as f1:
        with open("name_length.txt", "w") as f2:
            f2.write("\n".join([str(len(name))
                     for name in f1.read().split("\n")]))


def get_names_by_length(length):
    with open(FILENAME, "r") as f:
        return "\n".join(list(filter(lambda x: len(x) == length, f.read().split("\n"))))


print(get_longest_name() + "\n")
print(str(get_names_length_sum()) + "\n")
print(get_shortest_names() + "\n")
print(get_names_by_length(4) + "\n")

write_name_lengths()
