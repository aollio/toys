#!/usr/bin/env python3


from .lexer import *

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


class Type(AST):
    """The Type AST node represents a variable type (INTEGER or REAL)"""

    def __init__(self, token):
        self.token = token
        self.value = token.value


class Assign(AST):
    """The assign statement. left is a variable, right is a express"""

    def __init__(self, left, token, right):
        self.left = left
        self.token = token
        self.right = right


class VarDeclare(AST):
    """The declare statement. left is variable list, right is variable type"""

    def __init__(self, variables: list, type: Type):
        self.variable_list = [var for var in variables]
        self.type = type


class Compound(AST):
    """Represent compound statements, Like `BEGIN ... END`"""

    def __init__(self):
        self.children = []


class Block(AST):
    def __init__(self, declarations=[], compound=EmptyOp()):
        self.declarations = declarations
        self.compound = compound


class Param(AST):
    def __init__(self, var_node, type_node):
        self.type_node = type_node
        self.var_node = var_node


class ProcedureDeclare(AST):
    def __init__(self, proc_name, params: list, block):
        self.params = params
        self.block = block
        self.proc_name = proc_name


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
            result.append(self.procedure_declaration())

        return result

    def procedure_declaration(self):
        """
        Procedure declaration statement.
            <procedure> -> PROCEDURE <variable> (LPAREN <formal_parameter_list> RPAREN)? SEIM <block> SEIM
        :return:
        """
        self.eat(PROCEDURE)
        name = self.variable().value

        # 获取procedure的参数
        params = []
        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            params = self.formal_parameter_list()
            self.eat(RPAREN)

        self.eat(SEIM)
        block = self.block()
        self.eat(SEIM)
        return ProcedureDeclare(proc_name=name, block=block, params=params)

    def formal_parameter_list(self) -> list:
        """
        Formal parameter list of procedure.
            <formal_parameter_list> -> <formal_parameters>
                                    -> <formal_parameters> SEIM <formal_parameters_list>
        :return:
        """
        params = []
        params.extend(self.formal_parameters())

        if self.current_token.type == SEIM:
            self.eat(SEIM)
            params.extend(self.formal_parameter_list())

        return params

    def formal_parameters(self) -> list:
        """
        Formal parameters.
            <formal_parameters> -> <variable> (COMMA <variable>)* COLON <variable_type>
        :return:
        """
        params_nodes = []

        params_vars = []
        params_vars.append(self.variable())
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            params_vars.append(self.variable())

        self.eat(COLON)
        type = self.variable_type()
        for var in params_vars:
            params_nodes.append(Param(var_node=var, type_node=type))

        return params_nodes

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
        return VarDeclare(variables, type)

    def variable_type(self):
        """
        Variable type.
            <variable_type> -> REAL | INTEGER
        :return:
        """
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
            return Type(token)
        elif self.current_token.type == REAL:
            self.eat(REAL)
            return Type(token)

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
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node
