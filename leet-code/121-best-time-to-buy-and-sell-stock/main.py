#!/usr/bin/env python3

"""
Say you have an array for which the ith element is the price of a given stock on day i.

If you were only permitted to complete at most one transaction (ie, buy one and sell one share of the stock),
 design an algorithm to find the maximum profit.

Example 1:
Input: [7, 1, 5, 3, 6, 4]
Output: 5

max. difference = 6-1 = 5 (not 7-1 = 6, as selling price needs to be larger than buying price)

Example 2:
Input: [7, 6, 4, 3, 1]
Output: 0

In this case, no transaction is done, i.e. max profit = 0.

"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Solution:
    def maxProfit(self, prices: list):
        """
        :type prices: List[int]
        :rtype: int
        """
        maxvalue = 0
        days = len(prices)
        for curr in range(days):
            for nextday in range(curr + 1, days):
                delta = prices[nextday] - prices[curr]
                if delta > maxvalue:
                    maxvalue = delta
        return maxvalue


def test(prices: list, value: int):
    sol = Solution()
    assert sol.maxProfit(prices) == value


def main():
    test([7, 1, 5, 3, 6, 4], 5)
    test([7, 6, 4, 3, 1], 0)


if __name__ == '__main__':
    main()
