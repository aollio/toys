#!/usr/bin/env python3

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

# EOF-TOKEN is used to indicate the end of a file
INTEGER, OPERATOR, EOF = 'INTEGER', 'OPERATOR', 'EOF'

OPERATORLIST = [x for x in '+-/*']
WHITE = [' ']


def operator(a, op, b):
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
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, EOF
        self.type = type
        # token value: 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, + or None
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()


class Interpreter:
    def __init__(self, text):
        # client string input, e.g. '3+5'
        self.text = text
        # self.pos is an index in self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """
        Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence apart into tokens.
        One token at a time.
        :return:
        """
        text = self.text
        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more input left
        # to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # 如果是空白符, 则直接跳过
        if current_char in WHITE:
            self.pos += 1
            return self.get_next_token()

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit
        # and return the INTEGER token
        if current_char.isdigit():
            token_value = current_char
            # 如果下一个字符的位置也是一个数字, 将下一个的字符和现在相加,
            # 知道字符串到了结束位置或则下一个字符串不是数字
            self.pos += 1
            while self.pos < len(text) and text[self.pos].isdigit():
                token_value += text[self.pos]
                self.pos += 1

            token = Token(INTEGER, int(token_value))
            return token

        # 如果当前字符是操作符之一
        if current_char in OPERATORLIST:
            token = Token(OPERATOR, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token type
        # and if they match then 'eat' the current token and assign
        # the next token to the self.current_token,
        # raise raise an exception
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """
        expr -> INTEGER PLUS INTEGER
        :return:
        """
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be a single-digit integer
        left = self.current_token
        self.eat(INTEGER)

        # we expect the current token to be a '+' token
        op = self.current_token
        self.eat(OPERATOR)

        right = self.current_token
        self.eat(INTEGER)

        # after the above call the self.current_token is set to
        # EOF token

        result = operator(left.value, op.value, right.value)
        return result


def main():
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
