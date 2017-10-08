#!/usr/bin/env python3

"""
Simple Pascal Interpreter
"""
from collections import OrderedDict

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


# operators. integer div is integer div.
PLUS, MINUS, MUL, INTEGER_DIV, FLOAT_DIV = 'PLUS', 'MINUS', 'MUL', 'INTEGER_DIV', 'FLOAT_DIV'
DOT, COMMA, SEIM, LPAREN, RPAREN, COLON = 'DOT', 'COMMA', 'SEIM', 'LPAREN', 'RPAREN', 'COLON'
ASSIGN = 'ASSIGN'
EOF = 'EOF'
# identity, variable type token
ID = 'ID'
# integer类型的token
NUM_TOKEN_TYPE = 'NUM'
# 单个符号标记
SINGLE_MARK_DICT = {
    '+': Token(type=PLUS, value='+'),
    '-': Token(type=MINUS, value='-'),
    '*': Token(type=MUL, value='*'),
    '/': Token(type=FLOAT_DIV, value='/'),
    '.': Token(type=DOT, value='.'),
    ';': Token(type=SEIM, value=';'),
    '(': Token(type=LPAREN, value='('),
    ')': Token(type=RPAREN, value=')'),
    ',': Token(type=COMMA, value=','),
    ':': Token(type=COLON, value=':')
}
# 保留字
BEGIN, END = 'BEGIN', 'END'
PROGRAM, PROCEDURE = 'PROGRAM', 'PROCEDURE'
VAR = 'VAR'
# variable type
INTEGER = "INTEGER"
REAL = 'REAL'
# Reserve key
RESERVE_DICT = {
    BEGIN: Token(type=BEGIN, value=BEGIN),
    END: Token(type=END, value=END),
    PROGRAM: Token(type=PROGRAM, value=PROGRAM),
    'DIV': Token(type=INTEGER_DIV, value='//'),
    INTEGER: Token(type=INTEGER, value=INTEGER),
    REAL: Token(type=REAL, value=REAL),
    VAR: Token(type=VAR, value=VAR)
}


class Lexer:
    def __init__(self, text: str):
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
        while self.text[self.pos].isalnum() or self.text[self.pos] == '_':
            chars += self.text[self.pos]
            self.set_next_pos()
        chars = chars.upper()
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
        if current_char.isalpha() or current_char == '_':
            return self.id()

        # (multi)integer.
        if current_char.isdigit():
            return Token(type=NUM_TOKEN_TYPE, value=self.integer())

        # assign token
        if current_char == ':' and self.peek() == '=':
            self.set_next_pos()
            self.set_next_pos()
            return Token(ASSIGN, ':=')

        if current_char in SINGLE_MARK_DICT:
            self.set_next_pos()
            return SINGLE_MARK_DICT.get(current_char)

        self.error()

    def peek(self, seek=1):
        """向前看一个字符"""
        if self.pos + seek < len(self.text):
            return self.text[self.pos + seek]
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


class Declare(AST):
    """The declare statement. left is variable list, right is variable type"""

    def __init__(self, variable, type):
        self.variable_list = [var for var in variable]
        self.type = type


class Compound(AST):
    """Represent compound statements, Like `BEGIN ... END`"""

    def __init__(self):
        self.children = []


class Block(AST):
    def __init__(self, declarations=[], compound=EmptyOp()):
        self.declarations = declarations
        self.compound = compound


class Procedure(AST):
    def __init__(self, name, block):
        self.block = block
        self.name = name


class Program(AST):
    def __init__(self, name, block):
        self.block = block
        self.name = name


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

    def program(self):
        """
        Program.
            <program> -> PROGRAM <variable> SEIM <block> DOT

        :return:
        """
        self.eat(PROGRAM)
        name = self.variable().value
        self.eat(SEIM)
        block = self.block()
        self.eat(DOT)
        node = Program(name=name, block=block)
        return node

    def block(self):
        """
        Code Block.
            <block> -> <declarations> <compound_statements>
        :return:
        """
        node = Block(declarations=self.declarations(), compound=self.compound_statements())
        return node

    def declarations(self):
        """
        Variable declare block.
            <declarations> -> VAR <variable_declaration>+ <procedure_declaration>*
                           -> <procedure_declaration>+
                           -> <empty>
        :return:
        """
        result = []
        if self.current_token.type == VAR:
            self.eat(VAR)
            result.append(self.variable_declaration())
            while self.current_token.type == ID:
                result.append(self.variable_declaration())

        while self.current_token.type == PROCEDURE:
            result.append(self.procedure())

        return result

    def procedure(self):
        """
        Procedure declaration statement.
            <procedure> -> PROCEDURE <variable> SEIM <block> SEIM
        :return:
        """
        self.eat(PROCEDURE)
        name = self.variable().value
        self.eat(SEIM)
        block = self.block()
        self.eat(SEIM)
        return Procedure(name=name, block=block)

    def variable_declaration(self):
        """
        Variable declaration statement.
            <variable_declaration> -> <variable> (COMMA <variable>)* COLON <variable_type> SEIM
        """
        variables = []
        variables.append(self.variable())
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            variables.append(self.variable())
        self.eat(COLON)
        type = self.variable_type()
        self.eat(SEIM)
        return Declare(variables, type)

    def variable_type(self):
        """
        Variable type.
            <variable_type> -> REAL | INTEGER
        :return:
        """
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
            return INTEGER
        elif self.current_token.type == REAL:
            self.eat(REAL)
            return REAL

        self.error()

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
            <term> -> <factor> ((INTEGER_DIV | FLOAT_DIV) <factor>)*
        :return:
        """
        node = self.factor()

        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
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

        elif self.current_token.type == NUM_TOKEN_TYPE:
            integer = self.current_token
            self.eat(NUM_TOKEN_TYPE)
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


class Symbol:
    def __init__(self, name, type=None):
        self.type = type
        self.name = name


class BuiltinSymbol(Symbol):
    def __init__(self, name):
        super(BuiltinSymbol, self).__init__(name)

    def __str__(self):
        return '<Builtin, %s>' % self.name

    __repr__ = __str__


class VarSymbol(Symbol):
    def __init__(self, name, type):
        super(VarSymbol, self).__init__(name, type)

    def __str__(self):
        return '<{name}: {type}>'.format(name=self.name, type=self.type)

    __repr__ = __str__


class SymbolTable:
    def __init__(self):
        self._symbols = OrderedDict()
        self._init_builtin_types()

    def _init_builtin_types(self):
        self.define(BuiltinSymbol('INTEGER'))
        self.define(BuiltinSymbol('REAL'))

    def define(self, symbol: Symbol):
        print('Define %s' % symbol)
        self._symbols[symbol.name] = symbol

    def lookup(self, name: str):
        print('Lookup %s' % name)
        symbol = self._symbols.get(name)
        return symbol

    def __str__(self):
        return '<Symbols: {symbols}>'.format(symbols=[value for value in self._symbols.values()])


class SymbolTableBuilder(Visitor):
    def __init__(self, symbols: SymbolTable):
        self.symbols = symbols

    def visit_var(self, node: Var):
        symbol = self.symbols.lookup(node.value)
        if symbol is None:
            raise NameError(repr(node.value))

    def visit_program(self, node: Program):
        self.visit(node.block)

    def visit_procedure(self, node: Procedure):
        self.visit(node.block)

    def visit_block(self, node: Block):
        for child in node.declarations:
            self.visit(child)
        self.visit(node.compound)

    def visit_declare(self, node: Declare):
        type_name = node.type
        type_sym = self.symbols.lookup(type_name)
        for var in node.variable_list:
            var_name = var.value
            self.symbols.define(VarSymbol(var_name, type_sym))

    def visit_compound(self, node: Compound):
        for child in node.children:
            self.visit(child)

    def visit_assign(self, node: Assign):
        self.visit(node.right)
        self.visit(node.left)

    def visit_num(self, node):
        pass

    def visit_unaryop(self, node: UnaryOp):
        self.visit(node.expr)

    def visit_op(self, node):
        self.visit(node.right)
        self.visit(node.left)

    def visit_emptyop(self, node):
        pass


def op_operate(left, op, right):
    if op == '+':
        return left + right
    elif op == '-':
        return left - right
    elif op == '*':
        return left * right
    elif op == '/':
        return left / right
    elif op == '//':
        return left // right


class Interpreter(Visitor):
    def __init__(self):
        self.global_scope = {}

    def visit_program(self, node: Program):
        print('running', node.name)
        self.visit(node.block)

    def visit_procedure(self, node: Procedure):
        self.visit(node.block)

    def visit_block(self, node: Block):
        for child in node.declarations:
            self.visit(child)
        self.visit(node.compound)

    def visit_compound(self, node: Compound):
        for child in node.children:
            self.visit(child)

    def visit_declare(self, node: Declare):
        for var in node.variable_list:
            self.global_scope[var.value] = None

    def visit_assign(self, node: Assign):
        self.global_scope[node.left.value] = self.visit(node.right)

    def visit_var(self, node: Var):
        if node.value in self.global_scope:
            return self.global_scope.get(node.value)
        raise NameError('Unknown Identity {name}'.format(name=node.value))

    def visit_unaryop(self, node: UnaryOp):
        if node.value == '-':
            return -1 * self.visit(node.expr)
        return self.visit(node.expr)

    def visit_op(self, node: Op):
        return op_operate(left=self.visit(node.left), op=node.value, right=self.visit(node.right))

    def visit_num(self, node: Num):
        return node.value

    def visit_emptyop(self, node):
        pass


def main():
    import argparse
    parser = argparse.ArgumentParser("Simple pascal interpreter.")
    parser.add_argument('file', help='the pascal file name')
    args = parser.parse_args()
    text = open(file=args.file, encoding='utf-8').read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter()
    interpreter.visit(parser.parse())
    print(interpreter.global_scope)


if __name__ == '__main__':
    main()
