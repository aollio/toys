#!/usr/bin/env python3

"""
Simple Robin Interpreter
"""
from pparser import *

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


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
        raise Exception('Visit function {func} not exist'.format(
            func='visit_' + type(node).__name__.lower()))


class Symbol:
    def __init__(self, name, type=None):
        self.type = type
        self.name = name


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super(BuiltinTypeSymbol, self).__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(class_name=self.__class__.__name__, name=self.name)


class VarSymbol(Symbol):
    def __init__(self, name, type):
        super(VarSymbol, self).__init__(name, type)

    def __str__(self):
        return '<{class_name}(name=\'{name}\', type=\'{type}\')>'.format(
            name=self.name, type=self.type, class_name=self.__class__.__name__)

    __repr__ = __str__


class FunctionSymbol(Symbol):
    """
    The type is None because in default function don't return anything.
    """

    def __init__(self, name, params=None, type=None):
        super(FunctionSymbol, self).__init__(name, type)
        # a list of formal parameters
        self.params = params if params is not None else []

    def __str__(self):
        return '<{class_name}(name={name}, parameters={params})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.params
        )

    __repr__ = __str__


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
    elif op == '==':
        return left == right
    elif op == '<=':
        return left <= right
    elif op == '<':
        return left < right
    elif op == '>':
        return left > right
    elif op == '>=':
        return left >= right


class ScopeDict:
    def __init__(self, parent=None, init=False):
        self.scope = dict()
        self.parent = parent
        if init:
            self._init_built_symbol()

    def _init_built_symbol(self):
        pass

    def define(self, symbol: Symbol):
        self.scope[symbol.name] = symbol

    def lookup(self, name: str):
        value = self.scope.get(name, None)
        if value is not None:
            return value
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            raise ValueError('Unknown Symbol name %r' % name)


class Memory(dict):
    def __init__(self, parent=None, init=False):
        super(Memory, self).__init__()
        self.parent = parent
        if init:
            self._init_built_symbol()

    def _init_built_symbol(self):
        self['print'] = print

    def get(self, k, **kwargs):
        value = super(Memory, self).get(k, None)
        if value is not None:
            return value

        if self.parent is not None:
            return self.parent.get(k, **kwargs)


class Interpreter(Visitor):
    def __init__(self, tree):
        # symbol table
        self.tree = tree
        # global memory
        self.memory = Memory(init=True)

    def intreperter(self):
        self.visit(self.tree)
        # print(self.memory)
        # for key, value in self.memory.items():
        #     print('%s = %s' % (key, value))

    def visit_program(self, node: Program):
        self.visit(node.block)

    def visit_block(self, node: Block):
        for statement in node.children:
            self.visit(statement)

    def visit_functioncallast(self, node: FunctionCallAST):
        return self.memory[node.name](*[self.visit(arg) for arg in node.args])

    def visit_if(self, node: If):
        condition = self.visit(node.condition)
        if condition:
            self.visit(node.right_block)
        else:
            self.visit(node.wrong_block)

    def visit_while(self, node: While):
        while self.visit(node.condition):
            self.visit(node.block)

    def visit_assign(self, node: Assign):
        """Assign value will check type of variable"""
        value = self.visit(node.right)
        self.memory[node.left.value] = value

    def visit_var(self, node: Var):
        value = self.memory.get(node.value)
        if value is not None:
            return value
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
    # parser
    root_node = parser.parse()
    # semantic analyzer
    interpreter = Interpreter(root_node)
    interpreter.intreperter()


if __name__ == '__main__':
    main()
