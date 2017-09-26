import numpy as np
from numpy import random
import functools

rand_list = functools.partial(random.randint, 10)


def swap(src, i, j):
    src[i], src[j] = src[j], src[i]


def validate(sortfunc, size=20):
    src = rand_list(size=size)
    print("src: ", src)
    a = np.sort(src)
    sortfunc(src)
    print("correct: ", a)
    print("sorted: ", src)

    for i in range(len(src)):
        if a[i] == src[i]:
            pass
        else:
            print(False)
            return False
    print(True)
    return True

# validate(rand_list(size=10), [1, 2, 2])
