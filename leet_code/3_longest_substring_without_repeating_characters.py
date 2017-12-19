#!/usr/bin/env python3
"""
Given a string, find the length of the longest substring without repeating characters.

Examples:

Given "abcabcbb", the answer is "abc", which the length is 3.

Given "bbbbb", the answer is "b", with the length of 1.

Given "pwwkew", the answer is "wke", with the length of 3. Note that the answer must be a substring, "pwke" is a subsequence and not a substring.

"""

__author__ = "Aollio Hou"
__email__ = "aollio@outlook.com"


class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        98ms
        :type s: str
        :rtype: int
        """
        used = {}
        start = max_lens = 0
        for index, char in enumerate(s):
            if char in used and used[char] >= start:
                start = used[char] + 1
            else:
                max_lens = max(max_lens, index - start + 1)
            used[char] = index
        return max_lens


    def another_lengthOfLongestSubstring(self, s):
        """
        180ms
        :type s: str
        :rtype: int
        """
        window = []
        max_count = 0
        for char in s:
            if char in window:
                # resize the side window
                window = window[window.index(char) + 1:]
            window.append(char)
            if len(window) > max_count:
                max_count = len(window)
        return max_count

if __name__ == '__main__':
    print(Solution().lengthOfLongestSubstring('aab'))
