from ply import yacc

from lexer import MyLexer

class MyParser(object):

    def __init__(self):
        self.lexer = MyLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, debug=False)
        self.parser.exito = True
        self.parser.ast = ''

    def p_Program_1(self, p):
        '''Program : ExpressionList'''
        p[0] = f'{p[1]}'

    def p_ExpressionsList_1(self, p):
        '''ExpressionList : '''
        p[0] = f''

    def p_ExpressionsList_2(self, p):
        '''ExpressionList : Expression'''
        p[0] = f'{p[1]}'

    def p_ExpressionList(self, p):
        '''ExpressionList : Expression ExpressionList'''
        p[0] = f'{p[1]}{p[2]}'

    def p_Expression_1(self, p):
        '''Expression : ID'''
        p[0] = f'{p[1]}'

    def p_Expression_2(self, p):
        '''Expression : Expression BinaryOp Expression'''
        p[0] = f'{p[1]}{p[2]}{p[3]}'


    def p_BinaryOp_1(self, p):
        '''BinaryOp : ARROW'''
        p[0] = f'{p[1]}'

    def p_BinaryOp_1(self, p):
        '''BinaryOp : CONJ'''
        p[0] = f'{p[1]}'

    def p_BinaryOp_1(self, p):
        '''BinaryOp : DISJ'''
        p[0] = f'{p[1]}'

    def p_BinaryOp_1(self, p):
        '''BinaryOp : NOT'''
        p[0] = f'{p[1]}'

    def p_error(self, p):
        if p:
            print(f"Syntax error at token '{p.value}' (type: {p.type}) on line {p.lineno}")
        else:
            print("Syntax error: unexpected end of file (EOF)")
        self.parser.exito = False

if __name__ == '__main__':
    myparser = MyParser()

    while True:
        try:
            s = input('Enter expression: ')
            myparser.parser.parse(s)

            if myparser.parser.exito:
                print(f'Sucess')

        except EOFError:
            break
