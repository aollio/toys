from sort.util import validate


def partition(src: list, low, high):
    lo = low + 1
    hi = high
    val = src[low]
    while True:
        while src[lo] < val:
            if lo == high:
                break
            lo += 1
        while src[hi] > val:
            hi -= 1
        if hi <= lo:
            break
        src[lo], src[hi] = src[hi], src[lo]
    src[low], src[hi] = src[hi], src[low]
    return hi


def sort(src: list):
    __sort_private(src, 0, len(src) - 1)


def __sort_private(src, lo, hi):
    if hi <= lo:
        return
    j = partition(src, lo, hi)
    __sort_private(src, lo, j - 1)
    __sort_private(src, j + 1, hi)


if __name__ == '__main__':
    validate(sort)
