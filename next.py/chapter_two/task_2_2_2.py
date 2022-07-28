
class Octopus:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

    def birthday(self):
        self.age += 1

    def get_age(self):
        return self.age


def main():
    octopus_one = Octopus("Octavio", 5)
    octopus_two = Octopus("Octaviada", 5)

    octopus_one.birthday()

    print(octopus_one.get_age())
    print(octopus_two.get_age())


if __name__ == "__main__":
    main()
