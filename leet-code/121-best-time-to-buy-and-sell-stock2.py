#!/usr/bin/env python3

"""
Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit.
You may complete as many transactions as you like (ie, buy one and sell one share of the stock multiple times).
However, you may not engage in multiple transactions at the same time (ie, you must sell the stock before you
buy again).

"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Solution:
    def maxProfit(self, prices: list):
        """
        :type prices: List[int]
        :rtype: int
        """
        best = 0
        for i in range(1, len(prices)):
            delta = prices[i] - prices[i - 1]
            if delta > 0:
                best += delta
        return best


def test(prices: list, value: int):
    sol = Solution()
    assert sol.maxProfit(prices) == value


def main():
    test([7, 1, 5, 3, 6, 4], 7)
    # test([7, 6, 4, 3, 1], 0)
    print('passed')


if __name__ == '__main__':
    main()
