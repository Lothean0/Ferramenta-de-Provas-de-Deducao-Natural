from propositional_logic_parser import Parser
from propositional_logic_semantic import SemanticAnalyzer
from propositional_logic_codegen import CodeGenerator

C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_BLUE = '\033[94m'
C_END = '\033[0m'

if __name__ == '__main__':
    try:
        s = "((p0 ⟺ p1) ∨ p2)"
        print(C_YELLOW + f'\nParsing content: ' + C_END + f'{s}\n')

        ast = Parser.parse(s, debug=False)

        if not ast:
            print('')
            raise ValueError(C_RED + f'Parse error' + C_END)

        print(C_GREEN + f'Parsing success\n' + C_END)

        print(C_YELLOW + f'Analyzing...\n' + C_END)
        ast = SemanticAnalyzer().analyze(ast)
        print(C_GREEN + f'Semantic Analyzing success\n' + C_END)

        print(C_YELLOW + f'Generating code ...\n' + C_END)
        code = CodeGenerator().generate_code(ast)
        print(f'{code}\n')
        print(C_GREEN + f'Generating code success\n' + C_END)


    except Exception as e:
        print(C_RED + f'An error occurred: {e}' + C_END)
