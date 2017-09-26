"""
三切分快速排序
"""


def swap(src, i, j):
    src[i], src[j] = src[j], src[i]


def three_quick_sort(src, low, high):
    if low >= high:
        return

    lt = low
    gt = high
    val = src[low]
    i = low + 1
    while i <= gt:
        if src[i] == val:
            i += 1
        elif src[i] < val:
            swap(src, lt, i)
            lt += 1
            i += 1
        else:
            swap(src, gt, i)
            gt -= 1
        print(src)
    print('-----------')
    three_quick_sort(src, low, lt - 1)
    three_quick_sort(src, gt + 1, high)


if __name__ == '__main__':
    a = [4, 5, 2, 4, 6, 8, 3, 4, 51]
    three_quick_sort(a, 0, len(a) - 1)
    print(a)
