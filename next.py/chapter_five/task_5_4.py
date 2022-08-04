
MAX_NUM = 999999999
MAX_COUNT = 10


def check_id_valid(id_number):
    """
    Checks if an ID number is valid.
    :param id_number: The ID number to check
    :type id_number: int
    :return: True if the ID is valid, False otherwise.
    :rtype: bool
    """

    # Converting the ID to a list allows us to iterate through its numbers.
    id_number = list(str(id_number))

    # Using enumerate to access each number's index, double the number if
    # its index is odd if starting from 0 or even if starting from 1.
    for i, num in enumerate(id_number):
        if i % 2 == 1:
            id_number[i] = int(num) * 2
        else:
            id_number[i] = int(num)

        # If the number is above 9 after doubling, add up its numbers.
        num = id_number[i]
        if num > 9:
            id_number[i] = num // 10 + num % 10

    # Returns true if the sum of all numbers divides cleanly by 10.
    return sum(id_number) % 10 == 0


class IDIterator:
    """
    ID Iterator class, used to generate valid ID numbers.
    Generates IDs upwards of the given number.
    Iterating until generated 10 IDs or reached the limit (999999999).
    """

    def __init__(self, user_id=123456780) -> None:
        self._id = user_id

        # We will be counting the amount of IDs to know when to stop.
        self._ids_count = 0

    def __iter__(self):
        return self

    def __next__(self):
        # Stop if we've generated 10 IDs or reached the last possible ID number.
        if self._ids_count >= MAX_COUNT or self._id >= MAX_NUM:
            raise StopIteration()

        # Try the next IDs until a valid ID is created.
        while not check_id_valid(self._id):
            self._id += 1

        # Make sure we count the iterations if we aren't running to the limit.
        self._ids_count += 1

        # Increment current ID value by one for the next iteration
        self._id += 1

        # Return the most recent valid ID.
        return self._id - 1


def id_generator(id_number=123456780):
    """
    Yields the next valid ID number between id_number and 999999999.
    :param id_number: ID number, starting point of ID numbers generation range
    :type id_number: int
    :return: Generator object holding the next valid ID number
    :rtype: Generator Object
    """
    for i in range(id_number, MAX_NUM):
        if check_id_valid(i):
            yield i


def main():
    # Get user's input:
    # ID number, method of generation.
    user_id = int(input("Enter ID: "))
    use_method = input("Generator or Iterator (gen/it)?: ").strip().lower()

    # Make sure we have a valid generation method
    while use_method not in "gen it":
        print("Invalid generation method!")
        use_method = input("Generator or Iterator (gen/it)?: ").strip().lower()

    try:
        if use_method == "gen":
            gen = id_generator(user_id)
            for _ in range(10):
                print(next(gen))

        elif use_method == "it":
            for i in IDIterator(user_id):
                print(i)

    except StopIteration:
        print("\nStopIteration Exception: ID numbers generation reached it's limit.")

    finally:
        print("\nFinished generating ID numbers.")
        print("Method: " + ("Iterator" if use_method == "it" else "Generator"))


if __name__ == "__main__":
    main()
