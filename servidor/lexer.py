import ply.lex as lex
from ply.lex import TOKEN

tokens = (

    'ID',
    'ARROW',
    'CONJ',
    'DISJ',
    'NOT',
    'LPAREN',
    'RPAREN',
)

t_ARROW = r'→'
t_CONJ = r'∧'
t_DISJ = r'∨'
t_NOT = r'~'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'

ident = r'[a-zA-Z][a-zA-Z0-9_]*'

@TOKEN(ident)
def t_ID(t):
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

if __name__ == '__main__':
    lexer = lex.lex()
    while True:
        data = input()
        lexer.input(data)
        for tok in lexer:
            print(f"Token: {tok.type}, Value: {tok.value}")