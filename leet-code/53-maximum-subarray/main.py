#!/usr/bin/env python3

"""
Find the contiguous subarray within an array (containing at least one number) which has the largest sum.

For example, given the array [-2,1,-3,4,-1,2,1,-5,4],
the contiguous subarray [4,-1,2,1] has the largest sum = 6.
"""
__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Solution:
    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        local_best, global_best = nums[0], nums[0]
        for index in range(1, len(nums)):
            local_best = max(local_best + nums[index], nums[index])
            global_best = max(global_best, local_best)
        return global_best


def test(nums, sum):
    sol = Solution()
    maxsum = sol.maxSubArray(nums)
    if maxsum != sum:
        print('right: %s, answer: %s' % (sum, maxsum))
        raise AssertionError


def main():
    test([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6)
    print('passed')


if __name__ == '__main__':
    main()
