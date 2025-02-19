import ply.lex as lex
from ply.lex import TOKEN

class MyLexer(object):

    def __init__(self):
        self.lexer = lex.lex(module=self, debug=False)

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

    def t_ID(self, t):
        r'[a-zA-Z][a-zA-Z0-9_]*'
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def test(self):

        while True:
            try:
                s = input('Enter expression: ')
                self.lexer.input(s)
                for token in self.lexer:
                    print(f"Token( Type: {token.type}, Value: {token.value} )")

            except EOFError:
                break

if __name__ == '__main__':
    lexer = MyLexer()
    lexer.test()