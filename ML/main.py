from functools import lru_cache
import time
@lru_cache(maxsize=None)
def fib(n):
    if n <= 2: return 1
    else:
        return fib(n-1) + fib(n-2)

i = 100
while True:
    print(str(i) + " = " + str(fib(i)))
    i += 100
    time.sleep(1)