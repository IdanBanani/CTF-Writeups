import itertools
from math import sqrt
from functools import reduce
start = 1
end = 119
primes = []
for val in range(start, end + 1):
    if val > 1:
        for n in range(2, val//2 + 2):
            if (val % n) == 0:
                break
            else:
                if n == val//2 + 1:
                    primes.append(val)
primes = [1, 2] + primes
print(primes)


flatten_iter = itertools.chain.from_iterable


def factors(n):
    return set(flatten_iter((i, n//i)
                            for i in range(1, int(n**0.5)+1) if n % i == 0))


answer = []
# for i in range(128):
#     print(factors(i))
#     for f in factors(i):
#         if f == 1:
#             continue
#         if f in primes:
#             break
#     else:
#         answer.append(i)
# print(answer)

for i in range(33, 128):
    if i % 2 == 0:
        print(chr(i), end=' ')
