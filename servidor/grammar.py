from ply import yacc
from lexer import tokens

def p_Program_1(p):
    '''Program : ExpressionList'''
    p[0] = f'{p[1]}'

def p_ExpressionsList_1(p):
    '''ExpressionList : '''
    p[0] = f''

def p_ExpressionsList_2(p):
    '''ExpressionList : Expression'''
    p[0] = f'{p[1]}'

def p_ExpressionList(p):
    '''ExpressionList : Expression ExpressionList'''
    p[0] = f'{p[1]}{p[2]}'

def p_Expression_1(p):
    '''Expression : ID'''
    p[0] = f'{p[1]}'

def p_Expression_2(p):
    '''Expression : Expression BinaryOp Expression'''
    p[0] = f'{p[1]}{p[2]}{p[3]}'

def p_BinaryOp_1(p):
    '''BinaryOp : ARROW'''
    p[0] = f'{p[1]}'

def p_BinaryOp_2(p):
    '''BinaryOp : CONJ'''
    p[0] = f'{p[1]}'

def p_BinaryOp_3(p):
    '''BinaryOp : DISJ'''
    p[0] = f'{p[1]}'

def p_BinaryOp_4(p):
    '''BinaryOp : NOT'''
    p[0] = f'{p[1]}'

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' (type: {p.type}) on line {p.lineno}")
    else:
        print("Syntax error: unexpected end of file (EOF)")
    p.exito = False

myparser = yacc.yacc()

if __name__ == '__main__':

    while True:
        myparser.exito = True
        try:
            s = input('Enter expression: ')
            myparser.parse(s)

            if myparser.exito:
                print(f'Sucess')
            else:
                print(f'Error')

        except EOFError:
            break
