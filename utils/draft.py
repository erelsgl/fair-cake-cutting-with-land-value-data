#!python3

import sys
print(sys.version)

from functools import lru_cache


@lru_cache()
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

[fib(n) for n in range(16)]
print(fib.cache_info())


class Multer:
    def __init__(self, a):
        self.a = a

    @lru_cache()
    def calc(self, b):
        return self.a*b

m2 = Multer(2)
m3 = Multer(3)

print (m2.calc(10))
print (m3.calc(10))

print (m2.calc(10))
print (m3.calc(10))

print(m2.calc.cache_info())
print(m3.calc.cache_info())


sys.exit(0)

import matplotlib.pyplot as plt
plt.plot([1,2,3,6])
plt.ylabel('some numbers')
plt.show()
