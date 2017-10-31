#!/usr/bin/env python3


__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


def partition(nums, low, high):
    std = nums[low]
    left, right = low + 1, high
    while left < right:
        while left < high and nums[left] < std:
            left += 1
        while right > low and nums[right] > std:
            right -= 1

        if left >= right:
            nums[low], nums[right] = nums[right], nums[low]
            break
        else:
            nums[left], nums[right] = nums[right], nums[left]
        # 交换
        left += 1
        right -= 1
    return right


def _quick_sort(nums: list, low: int, high: int):
    if low >= high:
        return
    part = partition(nums, low, high)
    _quick_sort(nums, low, part - 1)
    _quick_sort(nums, part + 1, high)


def qucik_sort(nums: list):
    # nums.sort()
    _quick_sort(nums, 0, len(nums) - 1)


def test(nums: list):
    archive = list(nums)
    archive.sort()
    qucik_sort(nums)
    assert archive == nums


def main():
    test([])
    test([1, 2])
    test([2, 1, 4, 5, 9, 1, 3, 4, 5])
    # import random
    # a = list(range(random.Random().randint(1, 100000)))
    # random.Random().shuffle(x=a)
    # test(a)
    print('passed')


if __name__ == '__main__':
    main()
