from typing import Any

import ply.lex as lex
from ply.lex import TOKEN

reserved: tuple[str, ...] = (
    'EVAR',
    'EBINOP',
    'EUNOP',
    'ABSURD_LITERAL'
)

tokens: tuple[str, ...] = reserved + (
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

t_ARROW:str = r'→'
t_CONJ:str = r'∧'
t_DISJ:str = r'∨'
t_NOT:str = r'~'
t_LONG:str = r'⟺'
t_ABSURD:str = r'⊥'
t_LPAREN:str = r'\('
t_RPAREN:str = r'\)'
t_COMMA:str = r','


identifier:str = r'[a-zA-Z][a-zA-Z0-9_]*'

reserved_map:dict[str, str] = {}
for r in reserved:
    reserved_map[r.lower()] = r


@TOKEN(identifier)
def t_ID(t: Any) -> Any:
    t.type = reserved_map.get(t.value.lower(), 'ID')
    return t

def t_newline(t: Any) -> None:
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t : Any) -> None:
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