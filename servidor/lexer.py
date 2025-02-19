import ply.lex as lex

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

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

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