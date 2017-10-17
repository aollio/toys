#!/usr/bin/env python3


from spi import Parser, Lexer, Interpreter, SemanticAnalyzer
import spi

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


def main():
    lexer = Lexer(open('text.pas', 'r', encoding='utf-8').read())
    parser = Parser(lexer)
    interpreter = Interpreter()
    interpreter.visit(parser.parse())
    print(interpreter.global_scope)


def symbol():
    lexer = Lexer(open('text.pas', 'r', encoding='utf-8').read())

    parser = Parser(lexer)
    tree = parser.parse()
    builder = SemanticAnalyzer(spi.ScopedSymbolTable())
    builder.visit(tree)

    print(builder.symtab)
    interpreter = Interpreter()
    interpreter.visit(node=tree)
    print(interpreter.global_scope)


if __name__ == '__main__':
    symbol()
