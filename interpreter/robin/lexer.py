#!/usr/bin/env python3


__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

from tokens import Token
import tokens as t


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
        self.tokens = []
        while self.current_char is not None:
            self._get_tokens()
        self.tokens.append(Token(type=t.EOF))

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
        token = t.PRESERVE_DICT.get(chars, Token(type=t.ID, value=chars))
        return token

    def newline_and_indent(self):
        if self.current_char == '\n':
            self.tokens.append(Token(type=t.NEWLINE, value=t.NEWLINE))
            self.next_pos()
        count = 0
        while self.current_char == ' ':
            count += 1
            self.next_pos()
        if count % 4 != 0:
            raise Exception("Wrong Indent")
        a = count // 4
        [self.tokens.append(Token(type=t.INDENT, value=t.INDENT)) for x in range(a)]

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
            return Token(type=t.REAL_CONST, value=float(chars))
        else:
            return Token(type=t.INTEGER_CONST, value=int(chars))

    def error(self):
        raise Exception("Invalid Character '%s'" % self.text[self.pos])

    def skip_comment(self):
        if self.current_char is not None and self.text[self.pos] == '#':
            self.next_pos()
            while self.current_char is not None and self.text[self.pos] != '\n':
                self.next_pos()
        # self.next_pos is `\n` character
        # so if the next line begin with `#`, eat the NEWLINE token
        if self.current_char == '\n' and self._peek_char() in (None, '#'):
            self.next_pos()

    def skip_space(self):
        while self.current_char == ' ':
            self.next_pos()

    def _get_tokens(self):
        """获取下一个token"""

        while self.current_char is not None:
            # self.skip_whitespace()
            self.skip_comment()

            current_char = self.current_char

            # id. keyword or variable
            if current_char.isalpha() or current_char == '_':
                self.tokens.append(self.id())
                return

            # (multi)integer.
            if current_char.isdigit():
                self.tokens.append(self.number())
                return

            # new line
            if current_char == '\n':
                self.newline_and_indent()
                return

            # double mark， like '==', '<='...
            if self.peek() is not None and self.current_char is not None and self.current_char + self._peek_char() in t.DOUBLE_MARK_DICT:
                mark = self.current_char + self._peek_char()
                self.next_pos()
                self.next_pos()
                self.tokens.append(t.DOUBLE_MARK_DICT.get(mark, ))
                return

            # single mark, like '=', '+'...
            if current_char in t.SINGLE_MARK_DICT:
                self.next_pos()
                self.tokens.append(t.SINGLE_MARK_DICT.get(current_char, ))
                return

            # comment
            if current_char == '#':
                self.skip_comment()
                self._get_tokens()
                return

            if current_char == ' ':
                self.skip_space()
                return self._get_tokens()
                # return SINGLE_MARK_DICT.get(current_char,)

            self.error()
            # 如果输入流结束, 返回一个EOF Token
            # if self.current_char is None:
            #     return Token(type=EOF)

    def _peek_char(self, seek=1):
        """向前看一个字符"""
        if self.pos + seek < len(self.text):
            return self.text[self.pos + seek]
        else:
            return None

    def peek(self, seek=1):
        if len(self.tokens) > seek + 1:
            return self.tokens[seek]
        else:
            return Token(type=t.EOF)

    def read(self):
        if self.tokens:
            return self.tokens.pop(0)
        return Token(type=t.EOF)
