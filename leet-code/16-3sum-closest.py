#!/usr/bin/env python3

"""
Given an array S of n integers, find three integers in S such that the sum is closest to a given number,
 target.
  Return the sum of the three integers. You may assume that each input would have exactly one solution.

    For example, given array S = {-1 2 1 -4}, and target = 1.

    The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).

"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Solution:
    def threeSumClosest(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        nums.sort()
        result = nums[0] + nums[1] + nums[2]
        for i in range(len(nums) - 2):
            l, r = i + 1, len(nums) - 1
            while l < r:
                sum = nums[i] + nums[l] + nums[r]
                if sum == target:
                    return sum
                if abs(sum - target) < abs(result - target):
                    result = sum
                if sum < target:
                    l += 1
                elif sum > target:
                    r -= 1
        return result


def test(nums, target, result):
    sol = Solution()
    test_res = sol.threeSumClosest(nums, target)

    try:
        assert result == test_res
    except AssertionError as e:
        print('test_result:', test_res, 'right_result:', result)
        raise e


def main():
    test([-1, 2, 1, -4], 1, 2)
    test([0, 1, 2], 0, 3)
    test([0, 2, 1, -3], 1, 0)
    test([1, 1, -1, -1, 3], -1, -1)
    print('passed')


if __name__ == '__main__':
    main()
