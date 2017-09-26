from sort.util import validate

temp = []


def merge(src: list, lo, mid, hi):
    """

    :param src:原数组
    :param lo: 第一部分开始索引
    :param mid: mid+1第二部分开始索引
    :param hi: 第二部分结束索引
    :return: None
    """
    lo_po, hi_po = lo, mid + 1
    for x in range(lo, hi + 1):
        # print(src)
        if lo_po > mid:
            src[x] = temp[hi_po]
            hi_po += 1
        elif hi_po > hi:
            src[x] = temp[lo_po]
            lo_po += 1
        elif src[lo_po] > src[hi_po]:
            src[x] = temp[hi_po]
            hi_po += 1
        else:
            src[x] = temp[lo_po]
            lo_po += 1


def sort_private(src: list, lo, hi):
    if lo >= hi:
        return
    mid = lo + (hi - lo) // 2
    sort_private(src, lo, mid)
    sort_private(src, mid + 1, hi)
    merge(src, lo, mid, hi)


def sort(src):
    temp.clear()
    for x in range(len(src)):
        temp.append(src[x])
    sort_private(src, 0, len(src) - 1)


if __name__ == '__main__':
    validate(sort)
