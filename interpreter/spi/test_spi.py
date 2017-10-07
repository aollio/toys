#!/usr/bin/env python3


from spi import Parser, Lexer, Interpreter

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

program = """
BEGIN
    BEGIN
        number := 2;
        a := number;
        b := 10 * a + 10 * number / 4;
        c := a - -b
    END;
    x := 11;
END.
"""


def main():
    lexer = Lexer(program)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpreter()
    print(interpreter.global_scope)


if __name__ == '__main__':
    main()
