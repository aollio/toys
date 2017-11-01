#!/usr/bin/env python3


from lexer import *

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


###############################################################################
#                                                                             #
#  Parser                                                                #
#                                                                             #
###############################################################################
class AST:
    pass


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Op(AST):
    def __init__(self, left, op, right):
        self.right = right
        self.token = op
        self.value = op.value
        self.left = left


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.expr = expr
        self.token = op
        self.value = op.value


class EmptyOp(AST):
    """Represent an empty statement. e.g. `BEGIN END` """
    pass


class Var(AST):
    """Represent a variable. the field `value` is variable's name"""

    def __init__(self, token):
        self.token = token
        self.value = token.value


class Assign(AST):
    """The assign statement. left is a variable, right is a express"""

    def __init__(self, left, token, right):
        self.left = left
        self.token = token
        self.right = right


class Program(AST):
    def __init__(self, statement_list: list):
        self.statement_list = statement_list


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax. Unknown identity %s' % self.current_token)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def statement_list(self):
        """
        Statement list.
            <statement_list> -> <statement> | <statement> (NEWLINE statement)*
        :return:
        """
        node = self.statement()
        result = [node]
        while self.current_token.type == NEWLINE:
            self.eat(NEWLINE)
            result.append(self.statement())

        return Program(result)

    def statement(self):
        """
        A statement.
             <statement> -> <assign_statement> | <empty>
        :return:
        """
        if self.current_token.type == ID:
            return self.assign_statement()
        else:
            return self.empty()

    def empty(self):
        return EmptyOp()

    def assign_statement(self):
        """
        Assign statement.
            <assign_statement> -> <variable> ASSIGN <expr>
        :return:
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        return Assign(left=left, token=token, right=right)

    def variable(self):
        """
        A variable.
            <variable> -> Identity
        :return:
        """
        vartoken = self.current_token
        self.eat(ID)
        return Var(token=vartoken)

    def expr(self):
        """
        A expression statement.
            <expr> -> <term> ((PLUS|MINUS) <term>)*
        :return:
        """
        node = self.term()

        while self.current_token.type in (MINUS, PLUS):
            # operator plus or minus
            op = self.current_token
            self.eat(self.current_token.type)
            right = self.term()
            node = Op(left=node, op=op, right=right)

        return node

    def term(self):
        """
        A term.
            <term> -> <factor> (SPACE (MUL|DIV) SPACE <factor>)*
        :return:
        """
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            op = self.current_token
            self.eat(self.current_token.type)
            right = self.factor()

            node = Op(left=node, op=op, right=right)

        return node

    def factor(self):
        """
        A factor.
            <factor> -> (+|-) <factor>
                     -> Integer
                     -> <variable>
                     -> LPAREN <expr> RPAREN
        :return:
        """

        if self.current_token.type in (PLUS, MINUS):
            op = self.current_token
            if self.current_token.type == PLUS:
                self.eat(PLUS)
                return UnaryOp(op=op, expr=self.factor())
            elif self.current_token.type == MINUS:
                self.eat(MINUS)
                return UnaryOp(op=op, expr=self.factor())

        elif self.current_token.type in (INTEGER_CONST, REAL_CONST):
            integer = self.current_token
            self.eat(self.current_token.type)
            return Num(integer)

        elif self.current_token.type == ID:
            return self.variable()
        elif self.current_token.type == LPAREN:
            self.eat(LPAREN)
            expr = self.expr()
            self.eat(RPAREN)
            return expr

    def parse(self):
        node = self.statement_list()
        if self.current_token.type != EOF:
            self.error()
        return node


def _parse(filename):
    with open(filename) as file:
        text = file.read()
        lexer = Lexer(text=text)
        parser = Parser(lexer)
        return parser.parse()


if __name__ == '__main__':
    a = _parse('abc.py')
    print(a)
