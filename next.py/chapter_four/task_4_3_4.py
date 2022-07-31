
def get_fibo():
    prev, up = 0, 1

    while True:
        yield prev
        prev, up = up, prev + up


fibo_gen = get_fibo()
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
print(next(fibo_gen))
