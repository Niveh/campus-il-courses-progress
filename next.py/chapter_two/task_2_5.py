
class Animal:
    """
    A class used to represent an Animal.
    """
    zoo_name = "Hayaton"

    def __init__(self, name, hunger=0) -> None:
        self._name = name
        self._hunger = hunger

    def get_name(self):
        return self._name

    def is_hungry(self):
        return self._hunger > 0

    def feed(self):
        self._hunger -= 1

    def talk(self):
        pass


class Dog(Animal):
    """
    A class used to represent a Dog, inherited from Animal.
    Has a special method called fetch_stick.
    """

    def __init__(self, name, hunger=0) -> None:
        super().__init__(name, hunger)

    def talk(self):
        print("woof woof")

    def fetch_stick(self):
        print("There you go, sir!")


class Cat(Animal):
    """
    A class used to represent a Cat, inherited from Animal.
    Has a special method called chase_laser.
    """

    def __init__(self, name, hunger=0) -> None:
        super().__init__(name, hunger)

    def talk(self):
        print("meow")

    def chase_laser(self):
        print("Meeeeow")


class Skunk(Animal):
    """
    A class used to represent a Skunk, inherited from Animal.
    Has a special method called stink.
    """

    def __init__(self, name, hunger=0, stink_count=6) -> None:
        super().__init__(name, hunger)
        self._stink_count = stink_count

    def talk(self):
        print("tsssss")

    def stink(self):
        print("Dear lord!")


class Unicorn(Animal):
    """
    A class used to represent a Unicorn, inherited from Animal.
    Has a special method called sing.
    """

    def __init__(self, name, hunger=0) -> None:
        super().__init__(name, hunger)

    def talk(self):
        print("Good day, darling")

    def sing(self):
        print("I'm not your toy...")


class Dragon(Animal):
    """
    A class used to represent a Dragon, inherited from Animal.
    Has a special method called breath_fire.
    """

    def __init__(self, name, hunger=0, color="Green") -> None:
        super().__init__(name, hunger)
        self._color = color

    def talk(self):
        print("Raaaawr")

    def breath_fire(self):
        print("$@#$#@$")


def main():
    zoo_lst = [Dog("Brownie", 10), Cat("Zelda", 3),
               Skunk("Stinky"), Unicorn("Keith", 7), Dragon("Lizzy", 1450)]

    zoo_lst += [Dog("Doggo", 80), Cat("Kitty", 80), Skunk("Stinky Jr.",
                                                          80), Unicorn("Clair", 80), Dragon("McFly", 80)]

    for animal in zoo_lst:
        if animal.is_hungry():
            print(type(animal).__name__, animal.get_name())

            while animal.is_hungry():
                animal.feed()

            animal.talk()

            if isinstance(animal, Dog):
                animal.fetch_stick()
            elif isinstance(animal, Cat):
                animal.chase_laser()
            elif isinstance(animal, Skunk):
                animal.stink()
            elif isinstance(animal, Unicorn):
                animal.sing()
            elif isinstance(animal, Dragon):
                animal.breath_fire()

    print(Animal.zoo_name)


if __name__ == "__main__":
    main()
