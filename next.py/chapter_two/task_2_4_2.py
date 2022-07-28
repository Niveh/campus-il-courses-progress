
class BigThing:
    """
    A class used to represent anything.
    """

    def __init__(self, anything) -> None:
        self._anything = anything

    def size(self):
        """
        Returns the initial value if it is of type int.
        Returns the length of the value if it is list, dict or str.
        """
        if type(self._anything) == int:
            return int
        elif type(self._anything) in [list, dict, str]:
            return len(self._anything)


class BigCat(BigThing):
    """
    A class used to represent a Big Cat, inherited from BigThing.
    """

    def __init__(self, anything, weight) -> None:
        super().__init__(anything)
        self._weight = weight

    """
    Returns "Very Fat" if the weight is above 20.
    Returns "Fat" if the weight is above 15 and below 20.
    Returns "OK" otherwise.
    """

    def size(self):
        if self._weight > 20:
            return "Very Fat"
        elif self._weight > 15:
            return "Fat"
        else:
            return "OK"


def main():
    my_thing = BigThing("balloon")
    print(my_thing.size())

    cutie = BigCat("mitzy", 22)
    print(cutie.size())


if __name__ == "__main__":
    main()
