#!/usr/bin/env python3

"""
There are two sorted arrays nums1 and nums2 of size m and n respectively.

Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).

Example 1:
nums1 = [1, 3]
nums2 = [2]

The median is 2.0
Example 2:
nums1 = [1, 2]
nums2 = [3, 4]

The median is (2 + 3)/2 = 2.5
"""


__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Solution:
    def findMedianSortedArrays(self, A: list, B: list):
        """
        :type A: List[int]
        :type B: List[int]
        :rtype: float
        """
        m, n = len(A), len(B)
        if m > n:
            A, B, m, n = B, A, n, m
        if n == 0:
            raise ValueError

        imin, imax, half = 0, m, (m + n + 1) // 2
        while imin <= imax:
            i = (imin + imax) // 2
            j = half - i
            if i < m and B[j - 1] > A[i]:
                imin = i + 1
            elif i > 0 and A[i - 1] > B[j]:
                imax = i - 1
            else:
                if i == 0:
                    max_of_left = B[j - 1]
                elif j == 0:
                    max_of_left = A[i - 1]
                else:
                    max_of_left = max(A[i - 1], B[j - 1])

                if (m + n) % 2 == 1:
                    return max_of_left

                if i == m:
                    min_of_right = B[j]
                elif j == n:
                    min_of_right = A[i]
                else:
                    min_of_right = min(A[i], B[j])

                return (max_of_left + min_of_right) / 2


def test(nums1, nums2, median):
    sol = Solution()
    assert sol.findMedianSortedArrays(nums1, nums2) == median


def main():
    test([1, 3], [2], 2)
    test([1, 2], [3, 4], 2.5)
    print('passed')
    pass


if __name__ == '__main__':
    main()
