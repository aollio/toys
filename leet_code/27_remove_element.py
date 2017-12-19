#!/usr/bin/env python3

"""
Given an array and a value, remove all instances of that value in place and return the new length.

Do not allocate extra space for another array, you must do this in place with constant memory.

The order of elements can be changed. It doesn't matter what you leave beyond the new length.

Example:
Given input array nums = [3,2,2,3], val = 3

Your function should return length = 2, with the first two elements of nums being 2.


"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Solution:
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """

        for index in range(len(nums) - 1, -1, -1):
            if nums[index] == val:
                nums.pop(index)
        return len(nums)


def test(test_list, val, right_list):
    sol = Solution()
    try:
        assert sol.removeElement(test_list, val) == len(right_list)
        assert sorted(test_list) == sorted(right_list)
    except Exception as e:
        print("test_list:", test_list, "val:", val, "right_list:", right_list)
        raise e


def main():
    test([3, 2, 2, 3], 3, [2, 2])
    test([], 5, [])
    test([1], 1, [])
    test([1], 2, [1])
    print('passed')


if __name__ == '__main__':
    main()
