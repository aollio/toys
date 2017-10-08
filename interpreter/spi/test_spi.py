#!/usr/bin/env python3


from spi import Parser, Lexer, Interpreter, SymbolTableBuilder
import spi

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

program = """
BEGIN
    begin
        number := 2;
        a := number;
        b := 10 * a + 10 * number / 4;
        c := a - -b
    END;
    x := 11;
    y := x * 2
end.
"""


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
    builder = SymbolTableBuilder(spi.SymbolTable())
    builder.visit(tree)

    print(builder.symbols)
    interpreter = Interpreter()
    interpreter.visit(node=tree)
    print(interpreter.global_scope)



if __name__ == '__main__':
    symbol()
