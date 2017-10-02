#!/usr/bin/env python3
"""
Reverse digits of an integer.

Example1: x = 123, return 321
Example2: x = -123, return -321

click to show spoilers.

Note:
The input is assumed to be a 32-bit signed integer. Your function should return 0 when the reversed integer overflows.


"""

__author__ = "Aollio Hou"
__email__ = "aollio@outlook.com"


class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        sign = 1 if x >= 0 else -1
        result = sign * int(str(sign * x)[::-1])
        return result if result.bit_length() < 32 else 0


if __name__ == '__main__':
    print(Solution().reverse(1534236469))
