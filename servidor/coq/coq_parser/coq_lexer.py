from typing import Any

import ply.lex as lex
from ply.lex import TOKEN

reserved = (
        'LEMMA', 'GOAL',
        'PROOF', 'QUIT',
        'EVar',
        'EBinOp', 'EUnOp'
)

tokens = reserved + (
    'ID', 'ARROW',
    'CONJ', 'DISJ',
    'NOT', 'LONG',
    #'ABSURD',
    'LPAREN',
    'RPAREN', 'COMMA',
    'COLON', 'DOT',
    'HYPHEN',
)

t_ARROW = r'→'
t_CONJ = r'∧'
t_DISJ = r'∨'
t_NOT = r'¬'
t_LONG = r'⟺'
# t_ABSURD = r'⊥'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_COLON = r':'
t_DOT = r'.'
t_HYPHEN = r'\-'

identifier = r'[a-zA-Z][a-zA-Z0-9_]*'

reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r

@TOKEN(identifier)
def t_ID(t):
    t.type = reserved_map.get(t.value.lower(), 'ID')
    return t

def t_newline(t: Any):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t: Any):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore = ' \t'

lexer = lex.lex()

if __name__ == '__main__':
    while True:
        try:
            data = input()
            lexer.input(data)
            for tok in lexer:
                print(f"Token: {tok.type}, Value: {tok.value}")
        except EOFError:
            break
