
def intersection(list1, list2):
    return {x for x in list1 for y in list2 if x == y}


print(intersection([1, 2, 3, 4], [8, 3, 9]))
print(intersection([5, 5, 6, 6, 7, 7], [1, 5, 9, 5, 6]))
