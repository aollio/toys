#!/usr/bin/env python3

"""
Given a sorted array, remove the duplicates in place such that each element appear only once and return the new length.

Do not allocate extra space for another array, you must do this in place with constant memory.

For example,
Given input array nums = [1,1,2],

Your function should return length = 2, with the first two elements of nums being 1 and 2 respectively.
It doesn't matter what you leave beyond the new length.

"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Solution(object):
    def removeDuplicates(self, nums: list):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0
        pre = nums[-1]
        count = 1
        for index in range(len(nums) - 2, -1, -1):
            num = nums[index]
            if num == pre:
                nums.pop(index)
            else:
                count += 1
                pre = num
        return count


def test(test, right, len1):
    sol = Solution()
    len_of_list = sol.removeDuplicates(nums=test)
    try:
        assert len_of_list == len1
        assert test == right
    except Exception as e:
        print("test: ", test, "right:", right, "right_len:", len1)
        raise e


def main():
    test([], [], 0)
    test([1, 2], [1, 2], 2)
    test([1], [1], 1)
    test([1, 1, 2], [1, 2], 2)


if __name__ == '__main__':
    main()
    print('passed')
