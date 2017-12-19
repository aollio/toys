#!/usr/bin/env python3

"""
Given an integer array nums, find the sum of the elements between indices i and j (i ≤ j), inclusive.

Example:
Given nums = [-2, 0, 3, -5, 2, -1]

sumRange(0, 2) -> 1
sumRange(2, 5) -> -1
sumRange(0, 5) -> -3
Note:
You may assume that the array does not change.
There are many calls to sumRange function.
"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class NumArray:
    def __init__(self, nums):
        """
        :type nums: List[int]
        """
        self.sums = []
        sum = 0
        for each_num in nums:
            sum += each_num
            self.sums.append(sum)

    def sumRange(self, i, j):
        """
        :type i: int
        :type j: int
        :rtype: int
        """
        if i == 0:
            return self.sums[j]
        else:
            return self.sums[j] - self.sums[i - 1]


# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(i,j)

def test(nums, i, j, sum):
    obj = NumArray(nums)
    assert sum == obj.sumRange(i, j)


def main():
    nums = [-2, 0, 3, -5, 2, -1]
    test(nums, 0, 2, 1)
    test(nums, 2, 5, -1)
    test(nums, 0, 5, -3)
    print('passed')


if __name__ == '__main__':
    main()
