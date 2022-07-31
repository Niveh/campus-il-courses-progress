

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
    Takes an ID number (int) and a count (int) of valid IDs to generate.
    ID defaults at 100000000 if not given.
    Count defaults at -1 if not given,
    iterating until reaching the limit (999999999).
    """

    def __init__(self, user_id=100000000, count=-1) -> None:
        self._id = user_id

        # We will be counting the amount of iterations to know when to stop.
        self._ids_count = 0
        self._ids_count_max = count

    def __iter__(self):
        return self

    def __next__(self):
        # Stop if we have reached the given valid IDs count requested,
        # or maximum amount of iterations.
        if self._ids_count_max != -1:
            if self._ids_count >= self._ids_count_max or self._id >= 999999999:
                raise StopIteration()

        # Try the next IDs until a valid ID is created.
        self._id += 1
        while not check_id_valid(self._id):
            self._id += 1

        # Make sure we count the iterations if we aren't running to the limit.
        if self._ids_count_max != -1:
            self._ids_count += 1

        # Handle edge case
        if self._id >= 999999999:
            raise StopIteration()

        # Return the most recent valid ID.
        return self._id


def id_generator(id_number=100000000):
    """
    Yields the next valid ID number between id_number and 999999999.
    :param id_number: ID number, starting point of ID numbers generation range
    :type id_number: int
    :return: Generator object holding the next valid ID number
    :rtype: Generator Object
    """
    for i in range(id_number, 999999999):
        if check_id_valid(i):
            yield i


def main():
    # Get user's input:
    # ID number,
    # method generation,
    # amount of ID numbers to generate.
    user_id = int(input("Enter ID: "))
    use_method = input("Generator or Iterator (gen/it)?: ").strip().lower()
    user_count = int(
        input("Enter amount of IDs to generate (-1 for all possible IDs): "))

    try:
        if use_method == "gen":
            gen = id_generator(user_id)

            # Make sure the input is either -1 or a positive number
            if user_count == -1:
                while True:
                    print(next(gen))

            elif user_count > 0:
                for _ in range(user_count):
                    print(next(gen))

            else:
                print("Invalid input for amount of IDs to generate!")

        elif use_method == "it":
            for i in IDIterator(user_id, user_count):
                print(i)

    except StopIteration:
        print("Finished generating ID numbers!")


if __name__ == "__main__":
    main()
