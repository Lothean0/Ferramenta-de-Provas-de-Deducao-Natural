from typing import Any

import ply.yacc as yacc
from coq_lexer import tokens

from servidor.coq.coq_ast.ast_nodes import (
    ProgramDeclaration,
    LemmaDeclaration,
    ProofDeclaration,
    InstructionDeclaration,
    QuitDeclaration,
    EVarDeclaration,
    EUnOpDeclaration, BodyDeclaration, BinOpDeclaration
)
from servidor.coq.coq_semantic.semantic_analyzer import SemanticAnalyzer


def p_Program_1(p: Any) -> None:
    '''Program : ExpressionList'''
    p[0] = ProgramDeclaration(
        declarations=p[1],
        lineno=p.lineno(1)
    )


def p_ExpressionList_1(p: Any) -> None:
    '''ExpressionList : Expression'''
    p[0] = [p[1]]


def p_Expression_1(p: Any) -> None:
    '''Expression : Lemma_Declaration'''
    p[0] = p[1]


def p_Expression_2(p: Any) -> None:
    '''Expression : PROOF DOT'''
    p[0] = ProofDeclaration(
        lineno=p.lineno(1),
    )


def p_Expression_3(p: Any) -> None:
    '''Expression : HYPHEN ID ID'''
    p[0] = InstructionDeclaration(
        name=p[2],
        params=p[3],
        lineno=p.lineno(1),
    )


def p_Expression_4(p: Any) -> None:
    '''Expression : QUIT DOT '''
    p[0] = QuitDeclaration(
        lineno=p.lineno(1),
    )


def p_Lemma_Declaration(p: Any) -> None:
    '''Lemma_Declaration : LEMMA ID Parameters COLON Body DOT'''
    p[0] = LemmaDeclaration(
        name=p[2],
        params=p[3],
        body=p[5],
        lineno=p.lineno(1),
    )


def p_Parameters_1(p: Any) -> None:
    '''Parameters : Parameters Parameter'''
    p[0] = p[1] + [p[2]]


def p_Parameters_2(p: Any) -> None:
    '''Parameters : Parameter'''
    p[0] = [p[1]]


def p_Parameter_1(p: Any) -> None:
    '''Parameter : ID'''
    p[0] = {"name": p[1]}


def p_Body_1(p: Any) -> None:
    '''Body : ID'''
    p[0] = EVarDeclaration(
        name=p[1],
        lineno = p.lineno(1)
    )


def p_Body_2(p: Any) -> None:
    '''Body : UnaryOp ID'''
    p[0] = EUnOpDeclaration(
        operation=p[1],
        name = EVarDeclaration(
            name=p[2],
            lineno = p.lineno(1),
        ),
        lineno = p.lineno(1),
    )


def p_Body_3(p: Any) -> None:
    '''Body : Body BinaryOp Body'''
    p[0] = BinOpDeclaration(
        left = p[1],
        operation=p[2],
        right=p[3],
        lineno = p.lineno(1),
    )


def p_Body_4(p: Any) -> None:
    '''Body : UnaryOp LPAREN Body RPAREN'''
    p[0] = EUnOpDeclaration(
        symbol=p[1],
        body=p[3],
        lineno = p.lineno(1),
    )


def p_Body_5(p: Any) -> None:
    '''Body : LPAREN Body RPAREN'''
    p[0] = BodyDeclaration(
        body = p[2],
        lineno = p.lineno(1)
    )


def p_BinaryOp_1(p: Any) -> None:
    '''BinaryOp : ARROW'''
    p[0] = '→'


def p_BinaryOp_2(p: Any) -> None:
    '''BinaryOp : CONJ'''
    p[0] = '∧'


def p_BinaryOp_3(p) -> None:
    '''BinaryOp : DISJ'''
    p[0] = '∨'


def p_BinaryOp_4(p: Any) -> None:
    '''BinaryOp : LONG'''
    p[0] = '⟺'


def p_UnariOp(p: Any) -> None:
    '''UnaryOp : NOT'''
    p[0] = '¬'


def p_empty(p: Any) -> None:
    '''empty :'''
    p[0] = None


def p_error(p: Any) -> None:
    if p:
        print(f"Syntax error at token '{p.value}' (type: {p.type}) on line {p.lineno}")
    else:
        print("Syntax error: unexpected end of file (EOF)")


parser = yacc.yacc()

if __name__ == '__main__':
    while True:
        try:
            print(f'\n\nlemma lm1 p1 p2 p3 : ((p1→p2)→p3).')
            print(f'lemma lm1 p1 p2 : ((p1→p2)→p3).')
            print(f'lemma lm1 p1 p2 p3 : ((p1→p2).\n\n')
            s = input('Enter expression: ')
            result = parser.parse(s)

            if result:

                analyzer = SemanticAnalyzer()
                analyzer.analyze(result)

                print(result)
            else:
                print('Error')

        except EOFError:
            break
