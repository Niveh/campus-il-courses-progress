
def parse_ranges(ranges_string):
    ranges_string = ranges_string.split(",")
    first_generator = (r.replace("-", " ").split(" ") for r in ranges_string)
    final = []

    for start, stop in first_generator:
        second_generator = (num for num in range(int(start), int(stop) + 1))
        for n in second_generator:
            final.append(n)

    return (num for num in final)


print(list(parse_ranges("1-2,4-4,8-10")))
print(list(parse_ranges("0-0,4-8,20-21,43-45")))
