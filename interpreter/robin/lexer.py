#!/usr/bin/env python3


__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

from tokens import *


###############################################################################
#                                                                             #
#  Lexer                                                                      #
#                                                                             #
###############################################################################




class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def next_pos(self):
        """将当前位置向后移一位"""
        if self.pos is None:
            return None
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.pos = None
            self.current_char = None
            return
        self.current_char = self.text[self.pos]

    def id(self):
        """从输入中获取一个标识符 Identity"""
        chars = ''
        while self.current_char.isalnum() or self.current_char == '_':
            chars += self.current_char
            self.next_pos()
        # token = RESERVE_DICT.get(chars, Token(type=ID, value=chars))
        return Token(type=ID, value=chars)

    def number(self):
        """从输入中获取一个数字串"""
        chars = ''
        while self.current_char is not None and self.text[self.pos].isdigit():
            chars += self.text[self.pos]
            self.next_pos()

        if self.current_char == '.':
            chars += self.current_char
            self.next_pos()
            while self.current_char is not None and self.current_char.isdigit():
                chars += self.current_char
                self.next_pos()
            return Token(type=REAL_CONST, value=float(chars))
        else:
            return Token(type=INTEGER_CONST, value=int(chars))

    def error(self):
        raise Exception("Invalid Character '%s'" % self.text[self.pos])

    def skip_comment(self):
        if self.current_char is not None and self.text[self.pos] == '#':
            self.next_pos()
            while self.current_char is not None and self.text[self.pos] != '\n':
                self.next_pos()

    def skip_whitespace(self):
        while self.current_char == ' ':
            self.next_pos()

    def get_next_token(self):
        """获取下一个token"""

        # self.skip_whitespace()
        self.skip_comment()

        # 如果输入流结束, 返回一个EOF Token
        if self.current_char is None:
            return Token(type=EOF)

        current_char = self.current_char

        # id. keyword or variable
        if current_char.isalpha() or current_char == '_':
            return self.id()

        # (multi)integer.
        if current_char.isdigit():
            return self.number()

        if current_char in SINGLE_MARK_DICT:
            self.next_pos()
            return SINGLE_MARK_DICT.get(current_char, )

        if current_char == '#':
            self.skip_comment()
            return self.get_next_token()

        if current_char == ' ':
            self.skip_whitespace()
            return self.get_next_token()

        self.error()

    def peek(self, seek=1):
        """向前看一个字符"""
        if self.pos + seek < len(self.text):
            return self.text[self.pos + seek]
        else:
            return None
