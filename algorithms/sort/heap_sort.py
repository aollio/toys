import math
import numpy as np


def swap(a, i, j):
    temp = a[i]
    a[i] = a[j]
    a[j] = temp


def max(i, j):
    if i > j:
        return i
    else:
        return j


def sink(src, index, size):
    tar = index
    # 判断是否含有子树
    while tar * 2 < size:
        ch = 2 * tar
        lrch = 2 * tar + 1
        # 这里选择两个子节点中较大的一个
        if lrch < size:
            if src[ch] < src[lrch]:
                ch = lrch
        if src[tar] < src[ch]:
            swap(src, tar, ch)
        tar = ch
        # print(array)


def sort(src):
    lensrc = len(src)
    # 先进行下沉sink排序
    size = lensrc // 2
    while size >= 1:
        sink(src, size, lensrc)
        size -= 1
    lensrc -= 1
    while lensrc > 1:
        swap(src, 1, lensrc)
        lensrc -= 1
        sink(src, 1, lensrc)


if __name__ == '__main__':
    temp = np.random.rand(5)
    a = [0.0]
    for x in temp:
        a.append(x)
    print(a)
    a.insert(0, 0.0)
    print(a)
    sort(a)
    print(a)
