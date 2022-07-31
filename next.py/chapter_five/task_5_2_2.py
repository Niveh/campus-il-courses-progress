
numbers = iter(list(range(1, 101)))

for i in numbers:
    next(numbers)
    next(numbers)
    print(i)
