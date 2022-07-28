
count_animals = 0


class Octopus:
    """
    A class used to represent an Octopus.
    """

    def __init__(self, name="Octavio", age=0) -> None:
        self._name = name
        self._age = age

        global count_animals
        count_animals += 1

    def birthday(self):
        self._age += 1

    def get_age(self):
        return self._age

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name


def main():
    octopus_one = Octopus("Octivo", 3)
    octopus_two = Octopus(age=4)

    octopus_two.set_name("Octavey")
    print(octopus_two.get_name())

    print(f"count_animals: {count_animals}")


if __name__ == "__main__":
    main()
