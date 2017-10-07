#!/usr/bin/env python3

"""
Simple Pascal Interpreter
"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


###############################################################################
#                                                                             #
#  Lexer                                                                      #
#                                                                             #
###############################################################################
class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=self.value)

    __repr__ = __str__


#
PLUS, MINUS, MUL, DIV = 'PLUS', 'MINUS', 'MUL', 'DIV'
DOT, SEIM, LPAREN, RPAREN = 'DOT', 'SEIM', 'LPAREN', 'RPAREN'
ASSIGN = 'ASSIGN'
EOF = 'EOF'
ID = 'ID'
INTEGER = 'INTEGER'
# 当个符号标记
SINGLE_MARK_ALLOW_CHARS = '+-*/.;()'
SINGLE_MARK_DICT = {
    '+': Token(type=PLUS, value='+'),
    '-': Token(type=MINUS, value='-'),
    '*': Token(type=MUL, value='*'),
    '/': Token(type=DIV, value='/'),
    '.': Token(type=DOT, value='.'),
    ';': Token(type=SEIM, value=';'),
    '(': Token(type=LPAREN, value='('),
    ')': Token(type=RPAREN, value=')'),
}

BEGIN, END = 'BEGIN', 'END'
# Reserve key
RESERVE_DICT = {
    'BEGIN': Token(type='BEGIN', value='BEGIN'),
    'END': Token(type='END', value='END')
}


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def set_next_pos(self):
        """将当前位置向后移一位"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.pos = None

    def id(self):
        """从输入中获取一个标识符 Identity"""
        chars = ''
        while self.text[self.pos].isalnum():
            chars += self.text[self.pos]
            self.set_next_pos()
        return RESERVE_DICT.get(chars, Token(type=ID, value=chars))

    def integer(self):
        """从输入中获取一个数字串"""
        chars = ''
        while self.text[self.pos].isdigit():
            chars += self.text[self.pos]
            self.set_next_pos()
        return int(chars)

    def error(self):
        raise Exception("Invalid Character '%s'" % self.text[self.pos])

    def skip_withespace(self):
        while self.pos is not None and self.text[self.pos] in ('\r', '\n', ' '):
            self.set_next_pos()

    def get_next_token(self):
        """获取下一个token"""
        text = self.text

        self.skip_withespace()

        # 如果输入流结束, 返回一个EOF Token
        if self.pos is None:
            return Token(type=EOF)

        current_char = text[self.pos]

        # id. keyword or variable
        if current_char.isalpha():
            return self.id()

        # (multi)integer.
        if current_char.isdigit():
            return Token(type=INTEGER, value=self.integer())

        # assign token
        if current_char == ':' and self.peek() == '=':
            self.set_next_pos()
            self.set_next_pos()
            return Token(ASSIGN, ':=')

        if current_char in SINGLE_MARK_ALLOW_CHARS:
            self.set_next_pos()
            return SINGLE_MARK_DICT.get(current_char)

        self.error()

    def peek(self):
        """向前看一个字符"""
        if self.pos + 1 < len(self.text):
            return self.text[self.pos + 1]
        else:
            return None


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


class Compound(AST):
    """Represent compound statements, Like `BEGIN ... END`"""

    def __init__(self):
        self.children = []


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()

    def program(self):
        """
        Program.
            <program> -> <compound_statements> .
        :return:
        """
        compound_node = self.compound_statements()
        self.eat(DOT)
        return compound_node

    def compound_statements(self):
        """
        Compound statements.
            <compound_statements> -> BEGIN <statement_list> END
        :return:
        """
        compound = Compound()
        self.eat(BEGIN)
        statement_list = self.statement_list()
        self.eat(END)
        for statement in statement_list:
            compound.children.append(statement)
        return compound

    def statement_list(self):
        """
        Statement list.
            <statement_list> -> <statement> | <statement> (SEMI statement)*
        :return:
        """
        node = self.statement()
        result = [node]
        while self.current_token.type == SEIM:
            self.eat(SEIM)
            result.append(self.statement())

        return result

    def statement(self):
        """
        A statement.
             <statement> -> <compound_statement> | <assign_statement> | <empty>
        :return:
        """
        if self.current_token.type == BEGIN:
            return self.compound_statements()
        elif self.current_token.type == ID:
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
            <expr> -> <term> ((+|-) <term>)*
        :return:
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            op = self.current_token
            self.eat(self.current_token.type)
            right = self.term()

            node = Op(left=node, op=op, right=right)

        return node

    def term(self):
        """
        A term.
            <term> -> <factor> ((*|/) <factor>)*
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

        elif self.current_token.type == INTEGER:
            integer = self.current_token
            self.eat(INTEGER)
            return Num(integer)

        elif self.current_token.type == ID:
            return self.variable()
        elif self.current_token.type == LPAREN:
            self.eat(LPAREN)
            expr = self.expr()
            self.eat(RPAREN)
            return expr

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node


###############################################################################
#                                                                             #
#  Interpreter                                                                #
#                                                                             #
###############################################################################

class Visitor:
    def visit(self, node):
        visit_func = getattr(self, 'visit_' + type(node).__name__.lower(), self.generic_visit)
        return visit_func(node)

    def generic_visit(self, node):
        raise Exception('Visit function {func} not exist'.format(func='visit_' + type(node).__name__.lower()))


def op_operate(left, op, right):
    if op == '+':
        return left + right
    elif op == '-':
        return left - right
    elif op == '*':
        return left * right
    elif op == '/':
        return left / right


class Interpreter(Visitor):
    def __init__(self, parser: Parser):
        self.parser = parser
        self.global_scope = {}

    def visit_num(self, node: Num):
        return node.value

    def visit_unaryop(self, node: UnaryOp):
        if node.value == '-':
            return -1 * self.visit(node.expr)
        return self.visit(node.expr)

    def visit_op(self, node: Op):
        return op_operate(left=self.visit(node.left), op=node.value, right=self.visit(node.right))

    def visit_var(self, node: Var):
        if node.value in self.global_scope:
            return self.global_scope.get(node.value)
        raise NameError('Unknown Identity {name}'.format(name=node.value))

    def visit_emptyop(self, node):
        pass

    def visit_assign(self, node: Assign):
        self.global_scope[node.left.value] = self.visit(node.right)

    def visit_compound(self, node: Compound):
        for child in node.children:
            self.visit(child)

    def interpreter(self):
        self.visit(self.parser.parse())
