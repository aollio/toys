#!/usr/bin/env python3

"""
Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

The brackets must close in the correct order, "()" and "()[]{}" are all valid but "(]" and "([)]" are not.

"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        queue = []
        str_len = len(s)
        index = 0
        while index < str_len:
            char = s[index]
            if char in '}])':
                if len(queue) == 0 or '{[('['}])'.index(char)] != queue.pop():
                    return False
            else:
                queue.append(char)
            index += 1
        return len(queue) == 0


def main():
    sol = Solution()

    assert sol.isValid("()")
    assert sol.isValid("")
    assert sol.isValid("()[]{}")
    assert sol.isValid("(]") is False
    assert sol.isValid("[])") is False
    assert sol.isValid("(}]") is False
    assert sol.isValid("([)]") is False
    assert sol.isValid("]") is False
    assert sol.isValid("[") is False

    print('passed')


if __name__ == '__main__':
    main()
