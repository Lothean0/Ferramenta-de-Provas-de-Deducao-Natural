from typing import Any

import ply.lex as lex
from ply.lex import TOKEN

reserved = (
    'EVAR',
    'EBINOP',
    'EUNOP',
)

tokens = reserved + (
    'ID',
    'ARROW',
    'CONJ',
    'DISJ',
    'NOT',
    'LONG',
    'ABSURD',
    'LPAREN',
    'RPAREN',
    'COMMA'
)

t_ARROW = r'->'
t_CONJ = r'∧'
t_DISJ = r'∨'
t_NOT = r'~'
t_LONG = r'⟺'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','


identifier = r'[a-zA-Z][a-zA-Z0-9_]*'

reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r

def t_ABSURD(t):
    r'⊥'
    return t 

@TOKEN(identifier)
def t_ID(t):
    t.type = reserved_map.get(t.value.lower(), 'ID')
    return t

def t_newline(t: Any):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}'")


t_ignore = ' \t'

Lexer = lex.lex()
if __name__ == '__main__':
    while True:
        try:
            data = input()
            Lexer.input(data)
            for tok in Lexer:
                print(f"Token: {tok.type}, Value: {tok.value}")
        except EOFError:
            break