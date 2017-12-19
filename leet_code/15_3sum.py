#!/usr/bin/env python3

"""
Given an array S of n integers, are there elements a, b, c in S such that a + b + c = 0?
Find all unique triplets in the array which gives the sum of zero.

Note: The solution set must not contain duplicate triplets.

For example, given array S = [-1, 0, 1, 2, -1, -4],

A solution set is:
[
  [-1, 0, 1],
  [-1, -1, 2]
]
"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Solution:
    def threeSum(self, nums: list):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        result = []
        nums.sort()
        for index in range(len(nums)):
            # if index is equal num
            if index > 0 and nums[index] == nums[index - 1]:
                continue

            right = len(nums) - 1
            left = index + 1
            while left < right:
                sum = nums[index] + nums[left] + nums[right]
                if sum < 0:
                    # left need larger one
                    left += 1
                elif sum > 0:
                    # right need smaller one
                    right -= 1
                else:
                    # sum is zero. we need it
                    result.append([nums[index], nums[left], nums[right]])
                    # if has equal num
                    while left < right and nums[left + 1] == nums[left]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
        return result


def test(nums, right_nums: list):
    result = Solution().threeSum(nums)
    assert len(result) == len(right_nums)
    # assert three sum is zero
    for result_one_list in result:
        value = 0
        assert len(result_one_list) == 3
        for num in result_one_list:
            assert num in nums
            value += num
        assert value == 0
    # result must equal to right nums
    result = sorted(result)
    right_nums = sorted(right_nums)
    for index, one_list in enumerate(right_nums):
        assert sorted(right_nums[index]) == sorted(result[index])


def main():
    test([-1, 0, 1, 2, -1, -4], [[-1, 0, 1], [-1, -1, 2]])
    test([1], [])
    test([1, 2], [])
    test([0, 0, 0, 0], [[0, 0, 0]])
    test([1, 2, 3], [])
    test([1, 2, 3, -3], [[1, 2, -3]])
    test([-9, -14, -3, 2, 0, -11, -5, 11, 5, -5, 4, -4, 5, -15, 14, -8, -11, 10, -6, 1, -14, -12, -13, -11, 9, -7, -2,
          -13, 2, 2, -15, 1, 3, -3, -12, -12, 1, -2, 6, 14, 0, -4, -13, -10, -12, 8, -2, -8, 3, -1, 8, 4, -6, 2, 1, 10,
          2, 14, 4, 12, 1, 4, -2, 11, 9, -7, 6, -13, 7, -3, 8, 14, 8, 10, 12, 11, -4, -13, 10, 14, 1, -4, -4, 2, 5, 4,
          -11, -7, 3, 8, -10, 11, -11, -5, 7, 13, 3, -2, 8, -13, 2, 1, 9, -12, -11, 6],
         [[-15, 1, 14], [-15, 2, 13], [-15, 3, 12], [-15, 4, 11], [-15, 5, 10], [-15, 6, 9], [-15, 7, 8], [-14, 0, 14],
          [-14, 1, 13], [-14, 2, 12], [-14, 3, 11], [-14, 4, 10], [-14, 5, 9], [-14, 6, 8], [-14, 7, 7], [-13, -1, 14],
          [-13, 0, 13], [-13, 1, 12], [-13, 2, 11], [-13, 3, 10], [-13, 4, 9], [-13, 5, 8], [-13, 6, 7], [-12, -2, 14],
          [-12, -1, 13], [-12, 0, 12], [-12, 1, 11], [-12, 2, 10], [-12, 3, 9], [-12, 4, 8], [-12, 5, 7], [-12, 6, 6],
          [-11, -3, 14], [-11, -2, 13], [-11, -1, 12], [-11, 0, 11], [-11, 1, 10], [-11, 2, 9], [-11, 3, 8],
          [-11, 4, 7], [-11, 5, 6], [-10, -4, 14], [-10, -3, 13], [-10, -2, 12], [-10, -1, 11], [-10, 0, 10],
          [-10, 1, 9], [-10, 2, 8], [-10, 3, 7], [-10, 4, 6], [-10, 5, 5], [-9, -5, 14], [-9, -4, 13], [-9, -3, 12],
          [-9, -2, 11], [-9, -1, 10], [-9, 0, 9], [-9, 1, 8], [-9, 2, 7], [-9, 3, 6], [-9, 4, 5], [-8, -6, 14],
          [-8, -5, 13], [-8, -4, 12], [-8, -3, 11], [-8, -2, 10], [-8, -1, 9], [-8, 0, 8], [-8, 1, 7], [-8, 2, 6],
          [-8, 3, 5], [-8, 4, 4], [-7, -7, 14], [-7, -6, 13], [-7, -5, 12], [-7, -4, 11], [-7, -3, 10], [-7, -2, 9],
          [-7, -1, 8], [-7, 0, 7], [-7, 1, 6], [-7, 2, 5], [-7, 3, 4], [-6, -6, 12], [-6, -5, 11], [-6, -4, 10],
          [-6, -3, 9], [-6, -2, 8], [-6, -1, 7], [-6, 0, 6], [-6, 1, 5], [-6, 2, 4], [-6, 3, 3], [-5, -5, 10],
          [-5, -4, 9], [-5, -3, 8], [-5, -2, 7], [-5, -1, 6], [-5, 0, 5], [-5, 1, 4], [-5, 2, 3], [-4, -4, 8],
          [-4, -3, 7], [-4, -2, 6], [-4, -1, 5], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2], [-3, -3, 6], [-3, -2, 5],
          [-3, -1, 4], [-3, 0, 3], [-3, 1, 2], [-2, -2, 4], [-2, -1, 3], [-2, 0, 2], [-2, 1, 1], [-1, 0, 1]])
    print("passed")


if __name__ == '__main__':
    main()
