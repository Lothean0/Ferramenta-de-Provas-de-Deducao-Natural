import ply.yacc as yacc
from lexer import tokens

class Expr:
    def __repr__(self):
        return str(self)

class EVar(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"EVar({self.name})"

    def __repr__(self):
        return self.__str__()
    

class EBinOp(Expr):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return f"EBinOp({self.op}, {self.left}, {self.right})"

    def __repr__(self):
        return self.__str__()

    
class EUnOp(Expr):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __str__(self):
        return f"EUnOp({self.op}, {self.expr})"
    
    def __repr__(self):
        return self.__str__()


def p_Program_1(p):
    '''Program : ExpressionList'''
    p[0] = str(p[1])

def p_ExpressionList_1(p):
    '''ExpressionList : Expression'''
    p[0] = p[1]

def p_ExpressionList_2(p):
    '''ExpressionList : Expression ExpressionList'''
    p[0] = EBinOp(",", p[1], p[2])

def p_Expression_1(p):
    '''Expression : ID'''
    p[0] = EVar(p[1])

def p_Expression_2(p):
    '''Expression : UnaryOp ID'''
    p[0] = EUnOp(p[1], EVar(p[2]))

def p_Expression_3(p):
    '''Expression : Expression BinaryOp Expression'''
    p[0] = EBinOp(p[2], p[1], p[3])

def p_Expression_4(p):
    '''Expression : UnaryOp LPAREN Expression RPAREN'''
    p[0] = EUnOp(p[1], p[3])

def p_Expression_5(p):
    '''Expression : LPAREN Expression RPAREN'''
    p[0] = p[2]

def p_Program_2(p):
    '''Program : EExpressionList'''
    p[0] = p[1]

def p_EExpressionList_1(p):
    '''EExpressionList : EExpression'''
    p[0] = p[1]

def p_EExpressionList_2(p):
    '''EExpressionList : EExpression EExpressionList'''
    p[0] = p[1] + p[2]

def p_EVar(p):
    '''EExpression : EVar LPAREN ID RPAREN'''
    p[0] = p[3]

def p_EBinOp(p):
    '''EExpression : EBinOp LPAREN BinaryOp COMMA EExpression COMMA EExpression RPAREN'''
    p[0] = p[5] + p[3] + p[7]

def p_EUnOp(p):
    '''EExpression : EUnOp LPAREN UnaryOp COMMA EExpression RPAREN'''
    p[0] = p[3] + p[5]

def p_BinaryOp_1(p):
    '''BinaryOp : ARROW'''
    p[0] = '->'

def p_BinaryOp_2(p):
    '''BinaryOp : CONJ'''
    p[0] = '∧'

def p_BinaryOp_3(p):
    '''BinaryOp : DISJ'''
    p[0] = '∨'

def p_UnariOp(p):
    '''UnaryOp : NOT'''
    p[0] = '~'

# Error handling
def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' (type: {p.type}) on line {p.lineno}")
    else:
        print("Syntax error: unexpected end of file (EOF)")

myparser = yacc.yacc()

if __name__ == '__main__':
    while True:
        try:
            s = input('Enter expression: ')
            result = myparser.parse(s)

            if result:
                print(result)
            else:
                print('Error')

        except EOFError:
            break
