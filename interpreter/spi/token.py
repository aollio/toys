#!/usr/bin/env python3

"""
Token and Token types
"""
__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


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
    VAR: Token(type=VAR, value=VAR),
    PROCEDURE: Token(type=PROCEDURE, value=PROCEDURE)
}

# integer constant
REAL_CONST = 'REAL_CONST'
# real constant
INTEGER_CONST = 'INTEGER_CONST'
