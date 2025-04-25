from propositional_logic_parser import Parser
from propositional_logic_semantic import SemanticAnalyzer
from propositional_logic_codegen import CodeGenerator


if __name__ == '__main__':
    try:
        s_1 = "p0 -> p1"
        s_2 = "EBinOp(->, EVar(p0), EVar(p1))"
        s_3 = "⊥"
        s_4 = "ABSURD_LITERAL"
        s_5 = "p1"
        s_6 = "~p0"
        s_7 = "EUnOp(~, EVar(p0))"

        print(f'\nParsing content: {s_4}\n')

        ast = Parser.parse(s_7, debug=False)

        if not ast:
            print('')
            raise ValueError(f'Parse error')

        print(f'Parsing success\n')
        print(f'THIS IS WHAT I WANT\n {ast}')

        print(f'Analyzing...\n')
        ast = SemanticAnalyzer().analyze(ast)
        print(f'Semantic Analyzing success\n')

        print(f'Generating code ...\n')
        code = CodeGenerator().generate_code(ast)
        print(f'{code}\n')
        print(f'Generating code success\n')

        # EBinOp(->, EVar(p0), EVar(p1))


    except Exception as e:
        print(f'An error occurred: {e}')
