from typing import Any, Optional

from servidor.coq.coq_ast.ast_nodes import (
    ProgramDeclaration,
    LemmaDeclaration,
    ProofDeclaration,
    ApplyRuleDeclaration,
    QuitDeclaration,
    EVarDeclaration,
    EUnOpDeclaration,
    BodyDeclaration,
    BinOpDeclaration
)

class CodeGenerator:

    def __init__(self):
        self.xml = []


    def visit(self, node: Any) -> Optional[str]:

        if node is None:
            return None

        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):
        raise Exception(f'No visit method for node type: {type(node).__name__}')


    def emit(self, instruction, comment=None):
        if comment:
            self.xml.append(f"\t{instruction}  //{comment}")
        else:
            self.xml.append(f"\t{instruction}")


    def generate_code(self, ast) -> str:
        self.visit(ast)
        return "\n".join(self.xml)


    def visit_ProgramDeclaration(self, node: ProgramDeclaration):

        self.emit(f'[ProgramDeclaration]', f'Starting point')
        for decl in node.declarations:
            self.visit(decl)


    def visit_ProofDeclaration(self, node: ProofDeclaration) -> Any:
        self.emit(f'\t[Visiting] ProofDeclaration')


    def visit_QuitDeclaration(self, node: QuitDeclaration) -> Any:
        self.emit('[QuitDeclaration]', f'Ending point\n')


    def visit_LemmaDeclaration(self, node: LemmaDeclaration) -> Any:
        self.emit(f'\t[Visiting] LemmaDeclaration')
        self.visit(node.body)


    def visit_BodyDeclaration(self, node: BodyDeclaration) -> Any:
        self.emit(f'\t[Visiting] BodyDeclaration')

        self.visit(node.body)


    def visit_BinOpDeclaration(self, node: BinOpDeclaration) -> Any:
        self.emit(f'\t[Visiting] BinOpDeclaration')
        self.visit(node.left)
        self.visit(node.right)


    def visit_EVarDeclaration(self, node: EVarDeclaration) -> Any:
        self.emit(f'\t[Visiting] EVarDeclaration')


    def visit_EUnOpDeclaration(self, node: EUnOpDeclaration) -> Any:
        self.emit(f'\t[Visiting] EUnOpDeclaration')
        if node.body is not None:
            self.visit(node.body)


    def visit_ApplyRuleDeclaration(self, node: ApplyRuleDeclaration):

        self.emit(f'\t[Visiting] ApplyRuleDeclaration')
        function_name = node.name
        params = node.params

        if params:
            self.emit(f'\t\tCall {function_name}({params})', f'Apply rule: {function_name} with argument {params}')
        else:
            self.emit(f'\t\tCall {function_name}()', f'Apply rule: {function_name} with no arguments')


if __name__ == '__main__':
    appy_node_1 = ProgramDeclaration(declarations=[LemmaDeclaration(name='lm1', params=[{'var_name': 'p1'}, {'var_name': 'p2'}, {'var_name': 'p3'}], body=BodyDeclaration(body=BinOpDeclaration(operation='→', left=BodyDeclaration(body=BinOpDeclaration(operation='→', left=EVarDeclaration(name='p1', lineno=1), right=EVarDeclaration(name='p2', lineno=1), lineno=0), lineno=1), right=EVarDeclaration(name='p3', lineno=1), lineno=0), lineno=1), lineno=1), ProofDeclaration(lineno=2), ApplyRuleDeclaration(name='II', params='pp1', lineno=3), ApplyRuleDeclaration(name='EI', params='pp2', lineno=4), QuitDeclaration(lineno=5)], lineno=0)

    codegen = CodeGenerator()
    generated_code = codegen.generate_code(appy_node_1)

    print(generated_code)