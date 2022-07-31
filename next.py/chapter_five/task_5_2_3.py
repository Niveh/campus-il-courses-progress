import itertools

bills = [20, 20, 20, 10, 10, 10, 10, 10, 5, 5, 1, 1, 1, 1, 1]

solutions = set()

for r in range(1, len(bills) + 1):
    combos = itertools.combinations(bills, r)
    for c in combos:
        if sum(sorted(c)) == 100:
            solutions.add(c)

print(len(solutions))
