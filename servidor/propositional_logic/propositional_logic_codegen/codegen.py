from typing import Optional, Any, List
from servidor.propositional_logic.propositional_logic_ast import (
    ProgramDeclaration,
    EVarDeclaration,
    EUnOpDeclaration,
    ExpressionDeclaration,
    BinOpDeclaration,
    AbsurdDeclaration
)

C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_BLUE = '\033[94m'
C_END = '\033[0m'


class CodeGenerator:

    def __init__(self):
        self.problem = {}
        self.knowledge_base = {}

    def visit(self, node: Any) -> Optional[str]:
        if node is None:
            return None

        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit method for node type: {type(node).__name__}')

    def generate_code(self, ast) -> str:
        return self.visit(ast)

    def visit_ProgramDeclaration(self, node: ProgramDeclaration):
        result = []
        for decl in node.declarations:
            result.append(self.visit(decl))
        return "\n".join(result)

    def visit_ExpressionDeclaration(self, node: ExpressionDeclaration) -> Any:
        return self.visit(node.body)
    
    def visit_AbsurdDeclaration(self, node: AbsurdDeclaration) -> Any:
        return f"ABSURD_LITERAL"

    def visit_BinOpDeclaration(self, node: BinOpDeclaration) -> Any:
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"EBinOp({node.operation}, {left}, {right})"

    def visit_EVarDeclaration(self, node: EVarDeclaration) -> Any:
        return f"EVar({node.name})"

    def visit_EUnOpDeclaration(self, node: EUnOpDeclaration) -> Any:
        body = self.visit(node.body)
        return f"EUnOp({node.operation}, {body})"
