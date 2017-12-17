#!/usr/bin/env python3

"""
You are climbing a stair case. It takes n steps to reach to the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Note: Given n will be a positive integer.


Example 1:

Input: 2
Output:  2
Explanation:  There are two ways to climb to the top.

1. 1 step + 1 step
2. 2 steps
Example 2:

Input: 3
Output:  3
Explanation:  There are three ways to climb to the top.

1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step

"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Solution:
    def climbStairs(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n < 3:
            return n
        f2, f1 = 2, 1
        fn = f2
        fnminus1 = f1
        for index in range(3, n + 1):
            fn, fnminus1 = fn + fnminus1, fn
            # print(fn, fnminus1)
        return fn


def test(count, right_mth):
    sol = Solution()
    assert sol.climbStairs(count) == right_mth


def main():
    test(2, 2)
    test(3, 3)
    test(4, 5)


def say(msg=None):
    print('say %s' % msg)


if __name__ == '__main__':
    main()
