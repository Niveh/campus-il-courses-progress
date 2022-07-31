
def city_generator():
    print("Starting")
    yield "London"
    yield "Berlin"
    yield "Amsterdam"


def add_jerusalem_generator():
    yield from city_generator()
    yield "Jerusalem"


city = add_jerusalem_generator()
print(next(city))
print(next(city))
print(next(city))
print(next(city))
