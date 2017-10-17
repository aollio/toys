#!/usr/bin/env python3

"""
Simple Pascal Interpreter
"""
from collections import OrderedDict
from parser import *

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


class ProcedureSymbol(Symbol):
    """
    The type is None because in Pascal procedures don't return anything.
    """

    def __init__(self, name, params=None):
        super(ProcedureSymbol, self).__init__(name)
        # a list of formal parameters
        self.params = params if params is not None else []

    def __str__(self):
        return '<{class_name}(name={name}, parameters={params})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.params
        )

    __repr__ = __str__


class ScopedSymbolTable:
    def __init__(self, scope_name, scope_level, parent=None, init_builtin=False):
        self.parent = parent
        self.scope_level = scope_level
        self.scope_name = scope_name
        self._symbols = OrderedDict()
        if init_builtin:
            self._init_builtin_types()

    def _init_builtin_types(self):
        self.insert(BuiltinTypeSymbol('INTEGER'))
        self.insert(BuiltinTypeSymbol('REAL'))

    def insert(self, symbol: Symbol):
        # print('Define %s' % symbol)
        self._symbols[symbol.name] = symbol

    def lookup(self, name: str):
        # print('Lookup %s. (Scope name: %s)' % (name, self.scope_name))
        symbol = self._symbols.get(name)

        if symbol is None and self.parent is not None:
            return self.parent.lookup(name)

        return symbol

    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
                ('Scope name', self.scope_name),
                ('Scope level', self.scope_level),
                ('Parent Scope', self.parent.scope_name if self.parent else None)
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
        h2 = 'Scope (Scoped symbol table) contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend(
            ('%7s: %r' % (key, value)) for key, value in self._symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    __repr__ = __str__


class SemanticAnalyzer(Visitor):
    def __init__(self, tree):
        self.current_scope = None
        self.root_scope = None
        self.tree = tree

    def analyze(self):
        self.visit(self.tree)
        return self.root_scope

    def visit_program(self, node: Program):
        print('ENTER scope: global')
        global_scope = ScopedSymbolTable(scope_name='global', scope_level=1, init_builtin=True)
        self.current_scope = global_scope
        self.root_scope = global_scope
        # visit sub tree
        self.visit(node.block)

        print(global_scope)
        print('LEAVE scope: global')

    def visit_proceduredeclare(self, node: ProcedureDeclare):
        proc_name = node.proc_name
        proc_symbol = ProcedureSymbol(proc_name)
        self.current_scope.insert(proc_symbol)

        pre_scope = self.current_scope
        print('ENTER scope: %s' % proc_name)
        # Scope for parameters and local variables
        # todo 这里level不应该直接赋值为2
        procedure_scope = ScopedSymbolTable(
            scope_name=proc_name,
            scope_level=self.current_scope.scope_level + 1,
            parent=self.current_scope
        )
        self.current_scope = procedure_scope

        # Insert parameters into the procedure scope
        for param in node.params:
            param_type = self.current_scope.lookup(param.type_node.value)
            param_name = param.var_node.value
            var_symbol = VarSymbol(param_name, param_type)
            self.current_scope.insert(var_symbol)
            proc_symbol.params.append(var_symbol)

        self.visit(node.block)

        print(procedure_scope)
        print('LEAVE scope: %s' % proc_name)

        self.current_scope = pre_scope

    def visit_block(self, node: Block):
        for child in node.declarations:
            self.visit(child)
        self.visit(node.compound)

    def visit_vardeclare(self, node: VarDeclare):
        type_name = node.type.value
        type_sym = self.current_scope.lookup(type_name)

        for var in node.variable_list:
            var_name = var.value
            # if self.symtab.lookup(var_name) is not None:
            #     raise Exception(
            #         "Duplicate identifier '%s' found" % var_name
            #     )
            var_symbol = VarSymbol(var_name, type_sym)
            self.current_scope.insert(var_symbol)

    def visit_var(self, node: Var):
        var_name = node.value
        symbol = self.current_scope.lookup(var_name)
        if symbol is None:
            raise Exception(
                "Error: Symbol(identifier) not found '%s'" % var_name
            )

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


class Memory(dict):
    def __init__(self, parent=None):
        super(Memory, self).__init__()
        self.parent = parent

    def get(self, k, **kwargs):
        value = super(Memory, self).get(k, None)
        if value is not None:
            return value

        if self.parent is not None:
            return self.parent.get(k, **kwargs)


class Interpreter(Visitor):
    def __init__(self, tree, scope: ScopedSymbolTable):
        # symbol table
        self.tree = tree
        self.current_symtab = scope
        # global memory
        self.memory = Memory()

    def intreperter(self):
        self.visit(self.tree)
        print(self.memory)

    def visit_program(self, node: Program):
        print('Running', node.name)
        self.visit(node.block)

    def visit_proceduredeclare(self, node: ProcedureDeclare):
        """Procedure declare already is symbol in symbol table."""
        pass

    def visit_param(self):
        pass

    def visit_block(self, node: Block):
        for child in node.declarations:
            self.visit(child)
        self.visit(node.compound)

    def visit_compound(self, node: Compound):
        for child in node.children:
            self.visit(child)

    def visit_vardeclare(self, node: VarDeclare):
        pass

    def visit_assign(self, node: Assign):
        """Assign value will check type of variable"""
        value = self.visit(node.right)
        type_symbol = self.current_symtab.lookup(node.left.value).type
        if type_symbol.name == REAL and type(value) is float:
            self.memory[node.left.value] = value
            return
        if type_symbol.name == INTEGER and type(value) is int:
            self.memory[node.left.value] = value
            return
        raise TypeError('Wrong Assigned Type. Need %s Type, %s founded'
                        % (type_symbol, type(value).__name__))

    def visit_type(self, node: Type):
        pass

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
    semantic = SemanticAnalyzer(root_node)
    scopetab = semantic.analyze()
    interpreter = Interpreter(root_node, scopetab)
    interpreter.intreperter()


if __name__ == '__main__':
    main()
