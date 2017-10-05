#!/usr/bin/env python3


"""
支持加减乘除的计算器
包含词法分析, 语法分析.
解释运算通过运算符的优先级来实现.
对应文法:
    expr -> term ( (+|-) term )*
    term -> factor ( (*|/) factor )*
    factor -> int(int)* | \(expr\)
    int -> 0|1|2|3|4|5|6|7|8|9
"""

from enum import Enum

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class TokenType(Enum):
    INTEGER = 0,
    # '+-/*'
    OPERATOR = 1,
    EOF = 2,
    # 左括号
    LPAREN = 3,
    # 右括号
    RPAREN = 4,
    MUL = 5,
    DIV = 6


INTEGERS = '0123456789'
OPERATORS = '+-/*'
SKIPS = ' '


def calculate_operator(a, op, b):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '/':
        return a / b
    elif op == '*':
        return a * b

    raise InterruptedError('wrong operator %s' % op)


class Token:
    def __init__(self, type: TokenType, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({value}, {type})'.format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self.text = text
        # 指针指向下一次读取时的位置
        self.pos = 0

    def error(self):
        raise Exception('Invalid character')

    def get_integer(self):
        """
        获取整个数字, 直到遇到不是数字的地方为止
        :return:
        """
        tokenvalue = ''
        while self.pos < len(self.text) and self.text[self.pos] in INTEGERS:
            tokenvalue += self.text[self.pos]
            self.pos += 1
        return Token(type=TokenType.INTEGER, value=int(tokenvalue))

    def get_next_token(self):
        text = self.text
        # 如果文件已经结束了
        if self.pos > len(text) - 1:
            return Token(type=TokenType.EOF)

        current_char = self.text[self.pos]
        # 如果这个字符是数字, 这转交`get_integer`方法去执行
        if current_char in INTEGERS:
            return self.get_integer()
            # 如果这个字符是操作符
        elif current_char in OPERATORS:
            # 获取到字符后, 将指针向后移一位
            self.pos += 1
            return Token(type=TokenType.OPERATOR, value=current_char)
        elif current_char in '(':
            self.pos += 1
            return Token(type=TokenType.LPAREN, value=current_char)
        elif current_char in ')':
            self.pos += 1
            return Token(type=TokenType.RPAREN, value=current_char)
        # 如果是需要跳过的字符
        elif current_char in SKIPS:
            # 获取到字符后, 将指针向后移一位
            self.pos += 1
            return self.get_next_token()
        # 如果都不是, 所有读取到了错误的字符
        else:
            self.error()


class Interpreter:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, type: TokenType):
        """
        校对当前的token类型, 如果正确则`eat`当前的, 获取下一个字符
        :param type:
        :return:
        """
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        获取一个数字, 对应文法: factor -> 0|1|2|3|4|5|6|7|8|9
        :return:
        """
        if self.current_token.type is TokenType.INTEGER:
            value = self.current_token.value
            self.eat(TokenType.INTEGER)
            return value
        elif self.current_token.type is TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            value = self.expr()
            self.eat(TokenType.RPAREN)
            return value

    def operator_factor(self):
        """
        获取一个操作符, 对应文法: operator -> +|-|/|*
        :return:
        """
        value = self.current_token.value
        self.eat(TokenType.OPERATOR)
        return value

    def term(self):
        """
        获取一个乘除法的简单表达式, 对应文法 term -> factor((*|/)factor)*
        :return:
        """
        return self.atom(production_func=self.factor, allow_value='*/')

    def expr(self):
        """
        获取一个加减法的简单表达式, 对应文法 expr -> expr((+|-)expr)*
        :return:
        """
        return self.atom(production_func=self.term, allow_value='+-')

    def atom(self, production_func, allow_value=None):
        """
        atom. 获取一个简单表达式, 对应文法 atom -> production_func( (allow_value) production_func )*
        :param production_func:
        :param allow_value:
        :return:
        """
        result = production_func()

        while self.current_token.type is not TokenType.EOF and self.current_token.value in allow_value:
            op = self.operator_factor()
            right = production_func()
            result = calculate_operator(result, op, right)
        return result


def main():
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
