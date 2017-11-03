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


class If(AST):
    def __init__(self, condition, token, right_block, wrong_block):
        self.wrong_block = wrong_block
        self.right_block = right_block
        self.token = token
        self.condition = condition


class Block(AST):
    def __init__(self, children: list):
        self.children = children


class Program(AST):
    def __init__(self, children: Block):
        self.block = children


class Parser:
    def __init__(self, lexer: Lexer):
        self.indent = 0
        self.lexer = lexer
        self.current_token = lexer.read()

    def error(self):
        raise Exception('Invalid syntax. Unknown identity %s' % self.current_token)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.read()
        else:
            self.error()

    def program(self):
        """
        Program.
            <program> -> <block>
        :return:
        """
        return Program(self.block())

    def block(self):
        """
        A code Block.
            <block> -> <statement> | <statement> (NEWLINE statement)*
        :return:
        """
        inblock = self.check_indent()
        print(self.indent,self.check_indent())
        if inblock:
            self.eat_indent()
        else:
            return Block(children=[])

        node = self.statement()
        result = [node]
        while self.current_token.type == NEWLINE:
            self.eat(NEWLINE)
            inblock = self.check_indent()
            if inblock:
                self.eat_indent()
            else:
                break
            result.append(self.statement())
        return Block(children=result)

    def statement(self):
        """
        A statement.
             <statement> -> <assign_statement>
                         -> <if_statement>
                         -> <empty>
        :return:
        """
        if self.current_token.type == ID:
            return self.assign_statement()
        elif self.current_token.type == IF:
            return self.if_statement()
        else:
            return self.empty()

    def if_statement(self):
        """
        `if` statement:
            <if_statement> -> IF <expr> COLON NEWLINE INDENT <block> <elif_statement>

        :return:
        """
        token = self.current_token
        self.eat(IF)
        condition = self.expr()
        self.eat(COLON)
        self.eat(NEWLINE)
        print('aaa',self.current_token)
        self.indent += 1
        right_block = self.block()
        self.indent -= 1
        wrong_block = self.elif_statement()

        return If(condition=condition, token=token, right_block=right_block, wrong_block=wrong_block)

    def elif_statement(self):
        """
        `elif` statement:
            <elif_statement> -> ELIF <expr> COLON NEWLINE INDENT <block> <elif_statement>*
                             -> ELSE COLON NEWLINE INDENT <block>
                             -> <empty>
        :return:
        """
        if self.current_token.type == ELIF:
            token = self.current_token
            self.eat(ELIF)
            condition = self.expr()
            self.eat(COLON)
            self.eat(NEWLINE)
            self.indent += 1
            right_block = self.block()
            self.indent -= 1
            wrong_block = self.elif_statement()
            return If(condition, token, right_block, wrong_block)
        elif self.current_token.type == ELSE:
            self.eat(ELSE)
            self.eat(COLON)
            self.eat(NEWLINE)
            self.indent += 1
            block = self.block()
            self.indent -= 1
            return block
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

    def skip_space(self):
        while self.current_token.type == SPACE:
            self.eat(SPACE)

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
        node = self.block()
        # if self.current_token.type != EOF:
        #    self.error()
        return node

    def check_indent(self):
        indent = self.indent
        if indent == 0:
            return True
        if self.current_token.type != INDENT:
            return False
        count = 0
        seek = 0
        while self.lexer.peek(seek) == INDENT:
            count += 1
            seek += 1
        if count != indent - 1:
            return False
        return True

    def eat_indent(self):
        indent = self.indent
        while indent != 0 and self.current_token.type == INDENT:
            self.eat(INDENT)
            indent -= 1
        if indent:
            raise IndentationError()


def _parse(filename):
    with open(filename) as file:
        text = file.read()
        lexer = Lexer(text=text)
        parser = Parser(lexer)
        return parser.parse()


if __name__ == '__main__':
    a = _parse('abc.py')
    print(a)
