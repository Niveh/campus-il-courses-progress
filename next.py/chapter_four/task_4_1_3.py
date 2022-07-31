
def is_prime(n):
    # Corner case
    if n <= 1:
        return False
    # Check from 2 to n-1
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def first_prime_over(n):
    prime_gen = (num for num in range(n, n + 1000) if is_prime(num))
    return next(prime_gen)


print(first_prime_over(1000000))
