#!/usr/bin/env python3

import logging
from lexer import *
from uutil import log_def

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

log = logging.getLogger('Parser')

logging.basicConfig(level=logging.INFO)
###############################################################################
#                                                                             #
#  Parser                                                                     #
#                                                                             #
###############################################################################
class AST:

    def __repr__(self):
        return '<%s AST>' % self.__class__.__name__


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


class While(AST):
    def __init__(self, condition, token, block):
        self.block = block
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

    def error(self, need=None):
        msg = 'Invalid syntax. Unknown identity %r. ' % self.current_token
        if need:
            msg += 'Need Token %r' % need
        raise Exception(msg)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.read()
        else:
            self.error(token_type)

    @log_def
    def program(self):
        """
        Program.
            <program> -> <block>
        :return:
        """
        log.info('parsing program...')
        return Program(self.block())

    @log_def
    def block(self):
        """
        A code Block.
            <block> -> <statement> | <statement> (NEWLINE statement)*
        :return:
        """
        log.info('parsing block...')
        inblock = self.check_indent()
        if inblock:
            self.eat_indent()
        else:
            return Block(children=[])

        node = self.statement()
        result = [node]
        while self.current_token.type == t.NEWLINE:
            self.eat(t.NEWLINE)
            inblock = self.check_indent()
            if inblock:
                self.eat_indent()
            else:
                break
            result.append(self.statement())
        return Block(children=result)

    @log_def
    def statement(self):
        """
        A statement.
             <statement> -> <assign_statement>
                         -> <if_statement>
                         -> <while_statement>
                         -> <empty>
        :return:
        """
        if self.current_token.type == t.ID:
            return self.assign_statement()
        elif self.current_token.type == t.IF:
            return self.if_statement()
        elif self.current_token.type == t.WHILE:
            return self.while_statement()
        else:
            return self.empty()

    @log_def
    def while_statement(self):
        """
        `while` statement:
            <while_statement> -> WHILE <epxr> COLON NEWLINE INDENT <block>
        :return:
        """
        token = self.current_token
        self.eat(t.WHILE)
        condition = self.expr()
        self.eat(t.COLON)
        self.eat(t.NEWLINE)
        self.indent += 1
        right_block = self.block()
        self.indent -= 1

        return While(condition=condition, token=token, block=right_block)

    @log_def
    def if_statement(self):
        """
        `if` statement:
            <if_statement> -> IF <expr> COLON NEWLINE INDENT <block> <elif_statement>

        :return:
        """
        token = self.current_token
        self.eat(t.IF)
        condition = self.expr()
        self.eat(t.COLON)
        self.eat(t.NEWLINE)
        self.indent += 1
        right_block = self.block()
        self.indent -= 1
        wrong_block = self.elif_statement()

        return If(condition=condition, token=token, right_block=right_block, wrong_block=wrong_block)

    @log_def
    def elif_statement(self):
        """
        `elif` statement:
            <elif_statement> -> ELIF <expr> COLON NEWLINE INDENT <block> <elif_statement>*
                             -> ELSE COLON NEWLINE INDENT <block>
                             -> <empty>
        :return:
        """
        if self.current_token.type == t.ELIF:
            token = self.current_token
            self.eat(t.ELIF)
            condition = self.expr()
            self.eat(t.COLON)
            self.eat(t.NEWLINE)
            self.indent += 1
            right_block = self.block()
            self.indent -= 1
            wrong_block = self.elif_statement()
            return If(condition, token, right_block, wrong_block)
        elif self.current_token.type == t.ELSE:
            self.eat(t.ELSE)
            self.eat(t.COLON)
            self.eat(t.NEWLINE)
            self.indent += 1
            block = self.block()
            self.indent -= 1
            return block
        else:
            return self.empty()

    @log_def
    def empty(self):
        return EmptyOp()

    @log_def
    def assign_statement(self):
        """
        Assign statement.
            <assign_statement> -> <variable> ASSIGN <expr>
        :return:
        """
        left = self.variable()
        token = self.current_token
        self.eat(t.ASSIGN)
        right = self.expr()
        return Assign(left=left, token=token, right=right)

    @log_def
    def variable(self):
        """
        A variable.
            <variable> -> Identity
        :return:
        """
        vartoken = self.current_token
        self.eat(t.ID)
        return Var(token=vartoken)

    @log_def
    def expr(self):
        """
        A expression statement.
            <expr> -> <term_plus_minus> ((EQUAL|LESS_THAN|LESS_EQUAL|GREAT_THAN|GREAT_EQUAL) <term_plus_minus>)*
        :return:
        """
        node = self.term_plus_minus()

        while self.current_token.type in (t.EQUAL, t.LESS_THAN, t.LESS_EQUAL, t.GREAT_THAN, t.GREAT_EQUAL):
            # operator plus or minus
            op = self.current_token
            self.eat(self.current_token.type)
            right = self.term_plus_minus()
            node = Op(left=node, op=op, right=right)

        return node

    @log_def
    def term_plus_minus(self):
        """
        One or Two terms of addition or subtraction.
            <term_plus_minus> -> <term_mul_div> ((PLUS|MINUS) <term_mul_div>)*
        :return:
        """
        node = self.term_mul_div()

        while self.current_token.type in (t.MINUS, t.PLUS):
            # operator plus or minus
            op = self.current_token
            self.eat(self.current_token.type)
            right = self.term_mul_div()
            node = Op(left=node, op=op, right=right)

        return node

    @log_def
    def skip_space(self):
        while self.current_token.type == t.SPACE:
            self.eat(t.SPACE)

    @log_def
    def term_mul_div(self):
        """
        One or Two terms of multiplication or division.
            <term_mul_div> -> <factor> ((MUL|DIV) <factor>)*
        :return:
        """
        node = self.factor()

        while self.current_token.type in (t.MUL, t.DIV):
            op = self.current_token
            self.eat(self.current_token.type)
            right = self.factor()

            node = Op(left=node, op=op, right=right)

        return node

    @log_def
    def factor(self):
        """
        A factor.
            <factor> -> (+|-) <factor>
                     -> Integer
                     -> <variable>
                     -> LPAREN <expr> RPAREN
        :return:
        """

        if self.current_token.type in (t.PLUS, t.MINUS):
            op = self.current_token
            if self.current_token.type == t.PLUS:
                self.eat(t.PLUS)
                return UnaryOp(op=op, expr=self.factor())
            elif self.current_token.type == t.MINUS:
                self.eat(t.MINUS)
                return UnaryOp(op=op, expr=self.factor())

        elif self.current_token.type in (t.INTEGER_CONST, t.REAL_CONST):
            integer = self.current_token
            self.eat(self.current_token.type)
            return Num(integer)

        elif self.current_token.type == t.ID:
            return self.variable()
        elif self.current_token.type == t.LPAREN:
            self.eat(t.LPAREN)
            expr = self.expr()
            self.eat(t.RPAREN)
            return expr

    def parse(self):
        node = self.program()
        # if self.current_token.type != EOF:
        #     self.error(need=EOF)
        return node

    def check_indent(self):
        indent = self.indent
        if indent == 0:
            return True
        if self.current_token.type != t.INDENT:
            return False
        count = 0
        seek = 0
        while self.lexer.peek(seek) == t.INDENT:
            count += 1
            seek += 1
        if count != indent - 1:
            return False
        return True

    def eat_indent(self):
        indent = self.indent
        while indent != 0 and self.current_token.type == t.INDENT:
            self.eat(t.INDENT)
            indent -= 1
        if indent:
            raise IndentationError()

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

def _parse(filename):
    with open(filename) as file:
        text = file.read()
        lexer = Lexer(text=text)
        parser = Parser(lexer)
        return parser.parse()
