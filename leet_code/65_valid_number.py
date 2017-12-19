#!/usr/bin/env python3

"""
Validate if a given string is numeric.

Some examples:
"0" => true
" 0.1 " => true
"abc" => false
"1 a" => false
"2e10" => true
Note: It is intended for the problem statement to be ambiguous.
You should gather all requirements up front before implementing one.
"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Solution(object):
    def isNumber(self, s):
        """
        <num> -> [+|-]? <integer> [DOT <integer>?]? [E [+|-] <integer>]?
        <num> -> [+|-]? [DOT <integer>] [E [+|-] <integer>]?
        :type s: str
        :rtype: bool
        """
        s = s.strip()
        if not s:
            return False
        self.s = s
        self.index = 0
        self.curr_char = self.s[0]

        try:
            if self.curr_char in ['+', '-']:
                self.next_pos()

            if self.curr_char.isdigit():
                self.integer()

                if self.curr_char == '.':
                    self.next_pos()
                    self.integer()

                if self.curr_char in ['e', 'E']:
                    self.next_pos()
                    if self.curr_char in ['+', '-']:
                        self.next_pos()
                    self.integer(must=True)

            elif self.curr_char == '.':
                self.next_pos()
                self.integer(must=True)

                if self.curr_char in ['e', 'E']:
                    self.next_pos()
                    if self.curr_char in ['+', '-']:
                        self.next_pos()
                    self.integer(must=True)

        except RuntimeError:
            return False

        if self.curr_char is not None:
            return False
        else:
            return True

    def integer(self, must=False):
        char = ''
        while self.curr_char is not None and self.curr_char.isdigit():
            char += self.curr_char
            self.next_pos()
        if len(char) == 0 and must:
            raise RuntimeError

    def next_pos(self):
        self.index += 1
        if self.index < len(self.s):
            self.curr_char = self.s[self.index]
        else:
            self.curr_char = None

    def peek(self):
        if self.index < len(self.s):
            return self.s[self.index]
        else:
            return None


def test(num: str):
    sol = Solution()
    return sol.isNumber(num)


if __name__ == '__main__':
    assert test('0') is True
    assert test(' 0.1 ') is True
    assert test('2e10') is True
    assert test('2e10') is True
    assert test('22e10') is True
    assert test('.22e10') is True
    assert test('0.22e10') is True
    assert test('0.22e-10') is True
    assert test('3.') is True
    assert test('-1.') is True

    assert test('abc') is False
    assert test('') is False
    assert test('1 a') is False
    assert test('e9') is False
    assert test('.') is False
    assert test('0e') is False
    assert test('6.3.0') is False
