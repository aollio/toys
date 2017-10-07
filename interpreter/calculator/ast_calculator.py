#!/usr/bin/env python3

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = ('INTEGER', 'PLUS',
                                                       'MINUS', 'MUL', 'DIV',
                                                       'LPAREN', 'RPAREN', 'EOF')


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
        """

        :param text: client string input
        """
        self.text = text
        # 指针指向下一次读取时的位置
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
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
        This method is responsible for breaking a sentence apart into
        tokens. One token at a time.
        """
        text = self.text
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())



            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class AST:
    """
    Abstract Syntax Tree
    """
    pass


class BinOp(AST):
    """
    a binary operator is an operator that operates on two operands
    """

    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, expr, op):
        self.expr = expr
        self.op = op


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnaryOp(self.factor(), '-')
        elif token.type == PLUS:
            self.eat(PLUS)
            return UnaryOp(self.factor(), '+')
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if self.current_token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())
        return node

    def parser(self):
        return self.expr()


###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method.'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser: Parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        if node.op == '-':
            return -1 * self.visit(node.expr)
        else:
            return self.visit(node.expr)

    def interpret(self):
        tree = self.parser.parser()
        return self.visit(tree)


class ReversePolishNotation(NodeVisitor):
    def __init__(self, parser: Parser):
        self.parser = parser

    def visit_BinOp(self, node):
        return "{left} {right} {op}".format(left=self.visit(node.left), right=self.visit(node.right), op=node.op.value)

    def visit_Num(self, node):
        return str(node.value)

    def interpret(self):
        tree = self.parser.parser()
        return self.visit(tree)


class LISPNotation(NodeVisitor):
    def __init__(self, parser: Parser):
        self.parser = parser

    def visit_BinOp(self, node):
        return "({op} {left} {right})".format(left=self.visit(node.left), right=self.visit(node.right),
                                              op=node.op.value)

    def visit_Num(self, node):
        return str(node.value)

    def interpret(self):
        tree = self.parser.parser()
        return self.visit(tree)


def main():
    while True:
        try:
            try:
                text = input('spi> ')
            except NameError:  # Python3
                text = input('spi> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == '__main__':
    main()
