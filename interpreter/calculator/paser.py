#!/usr/bin/env python3

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

# EOF-TOKEN is used to indicate the end of a file
INTEGER, OPERATOR, EOF = 'INTEGER', 'OPERATOR', 'EOF'
MUL, DIV = 'MUL', 'DIV'


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


class Lexer:
    def __init__(self, text):
        # client string input, e.g. "3 * 5", "12 / 3 * 4", etc
        self.text = text
        # self.pos is an index into self.text.pas
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            self.error()

        return Token(EOF, None)


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        """lexeme parsing error."""
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token type
        # and if they match then 'eat' the current token and assign
        # the next token to the self.current_token,
        # raise raise an exception
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """parsing an Integer"""
        self.eat(INTEGER)


    def expr(self):
        self.factor()
        while self.current_token.type in (MUL, DIV):
            if self.current_token.type == MUL:
                self.eat(MUL)
                self.factor()
            elif self.current_token.type == DIV:
                self.eat(DIV)
                self.factor()

    def parse(self):
        self.expr()



def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue

        parser = Parser(Lexer(text))
        parser.parse()


if __name__ == '__main__':
    main()