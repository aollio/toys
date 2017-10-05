#!/usr/bin/env python3

"""
支持加减乘除的计算器
包含词法分析, 语法分析.
解释运算通过栈来实现
"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

INTEGER, OPERATOR, EOF = 'INTEGER', 'OPERATOR', 'EOF'

INTEGER_LIST = [x for x in '0123456789']
OPERATOR_LIST = [x for x in '+-/*']
SKIP_LIST = [' ']


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
    def __init__(self, type, value=None):
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
        while self.pos < len(self.text) and self.text[self.pos] in INTEGER_LIST:
            tokenvalue += self.text[self.pos]
            self.pos += 1
        return Token(type=INTEGER, value=int(tokenvalue))

    def get_next_token(self):
        text = self.text
        # 如果文件已经结束了
        if self.pos > len(text) - 1:
            return Token(type=EOF)

        current_char = self.text[self.pos]
        # 如果这个字符是数字, 这转交`get_integer`方法去执行
        if current_char in INTEGER_LIST:
            return self.get_integer()
            # 如果这个字符是操作符
        elif current_char in OPERATOR_LIST:
            # 获取到字符后, 将指针向后移一位
            self.pos += 1
            return Token(type=OPERATOR, value=current_char)
        # 如果是需要跳过的字符
        elif current_char in SKIP_LIST:
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

    def eat(self, type):
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
        value = self.current_token.value
        self.eat(INTEGER)
        return value

    def operator_factor(self):
        """
        获取一个操作符, 对应文法: operator -> +|-|/|*
        :return:
        """
        value = self.current_token.value
        self.eat(OPERATOR)
        return value

    def expr(self):

        operators = []
        values = []

        values.append(self.factor())

        while self.current_token.type is OPERATOR:
            # 将操作符入操作符栈
            operator = self.operator_factor()
            operators.append(operator)
            # 获取下一个数字
            integer = self.factor()
            values.append(integer)

            # 如果是 `*`, `/`, 则先计算一次
            if operator in ['*', '/']:
                self.calculate(operators, values)

        self.calculate(operators, values, allow_operator='+-/*')
        return values[0]

    def calculate(self, operators: list, values: list, allow_operator='*/'):
        while len(operators) > 0:
            operator = operators.pop()
            if operator not in allow_operator:
                operators.append(operator)
                return
            left_value = values.pop()
            right_value = values.pop()
            values.append(calculate_operator(right_value, operator, left_value))


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
