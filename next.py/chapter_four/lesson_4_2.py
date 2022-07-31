import random
import itertools

cube_game = (random.randint(1, 6) for i in range(4))

for permutation in itertools.permutations([0, 5, 6, 9]):
    print(permutation)

integers = (i for i in range(1, 11))
squared = (x * x for x in integers)
negated = (-x for x in squared)

for num in negated:
    print(num)
