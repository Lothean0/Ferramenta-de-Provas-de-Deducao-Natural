from typing import Any

import ply.yacc as yacc
from .lexer import tokens

from servidor.propositional_logic.propositional_logic_ast.ast_nodes import (
    ProgramDeclaration,
    EVarDeclaration,
    ExpressionDeclaration,
    EUnOpDeclaration,
    BinOpDeclaration,
    AbsurdDeclaration
)

def p_Program_1(p:Any) -> None:
    '''Program : ExpressionList'''
    p[0] = ProgramDeclaration(
        declarations=p[1],
        lineno=p.lineno(1),
    )

def p_ExpressionList_1(p:Any) -> None:
    '''ExpressionList : Expression'''
    p[0] = [p[1]]


def p_Expression_1(p:Any) -> None:
    '''Expression : ID'''
    p[0] = EVarDeclaration(
        name=p[1],
        lineno=p.lineno(1),
    )


def p_Expression_2(p:Any) -> None:
    '''Expression : Expression BinaryOp Expression'''
    p[0] = BinOpDeclaration(
        left=p[1],
        operation=p[2],
        right=p[3],
        lineno=p.lineno(1),
    )


def p_Expression_3(p:Any) -> None:
    '''Expression : UnaryOp ID'''
    p[0] = EUnOpDeclaration(
        operation=p[1],
        name=EVarDeclaration(
            name=p[2],
            lineno=p.lineno(1),
        ),
        body=None,
        lineno=p.lineno(1),
    )


def p_Expression_4(p:Any) -> None:
    '''Expression : UnaryOp LPAREN Expression RPAREN'''
    p[0] = EUnOpDeclaration(
        operation=p[1],
        name=None,
        body=p[3],
        lineno=p.lineno(1),
    )


def p_Expression_5(p:Any) -> None:
    '''Expression : LPAREN Expression RPAREN'''
    p[0] = ExpressionDeclaration(
        body=p[2],
        lineno=p.lineno(1)
    )

def p_Expression_6(p:Any) -> None:
    '''Expression : ABSURD'''
    p[0] = AbsurdDeclaration(
        name=p[1],
        lineno=p.lineno(1),
    )


def p_Program_2(p:Any) -> None:
    '''Program : EExpressionList'''
    p[0] = p[1]


def p_EExpressionList_1(p:Any) -> None:
    '''EExpressionList : EExpression'''
    p[0] = p[1]


def p_EExpressionList_2(p:Any) -> None:
    '''EExpressionList : EExpression EExpressionList'''
    p[0] = p[1] + p[2]


def p_EVar(p:Any) -> None:
    '''EExpression : EVAR LPAREN ID RPAREN'''
    p[0] = p[3]


def p_EBinOp(p:Any) -> None:
    '''EExpression : EBINOP LPAREN BinaryOp COMMA EExpression COMMA EExpression RPAREN'''
    p[0] = p[2] + p[5] + p[3] + p[7] + p[8]


def p_EUnOp(p:Any) -> None:
    '''EExpression : EUNOP LPAREN UnaryOp COMMA EExpression RPAREN'''
    p[0] = p[3] + p[5]

def p_Absurd(p:Any) -> None:
    '''EExpression : ABSURD'''
    p[0] = "⊥"


def p_BinaryOp_1(p:Any) -> None:
    '''BinaryOp : ARROW'''
    p[0] = '->'


def p_BinaryOp_2(p:Any) -> None:
    '''BinaryOp : CONJ'''
    p[0] = '∧'


def p_BinaryOp_3(p:Any) -> None:
    '''BinaryOp : DISJ'''
    p[0] = '∨'


def p_BinaryOp_4(p:Any) -> None:
    '''BinaryOp : LONG'''
    p[0] = '⟺'


def p_UnariOp(p:Any) -> None:
    '''UnaryOp : NOT'''
    p[0] = '~'


# Error handling
def p_error(p:Any) -> None:
    if p:
        print(f"Syntax error at token '{p.value}' (type: {p.type}) on line {p.lineno}")
    else:
        print("Syntax error: unexpected end of file (EOF)")


Parser = yacc.yacc()


if __name__ == '__main__':
    while True:
        try:
            s = input('Enter expression: ')
            result = Parser.parse(s)

            if result:
                print(result)
            else:
                print('Error')

        except EOFError:
            break
