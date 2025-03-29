from typing import Any, Optional

from servidor.coq.coq_ast.ast_nodes import (
    ProgramDeclaration,
    LemmaDeclaration,
    ProofDeclaration,
    InstructionDeclaration,
    QuitDeclaration,
    EVarDeclaration,
    BodyDeclaration,
    EUnOpDeclaration,
    BinOpDeclaration
)
from servidor.coq.coq_semantic.symbol_table import SymbolTable


class SemanticError(Exception):

    def __init__(
            self,
            message: str,
            node: Optional[Any] = None
    ) -> None:
        self.node = node
        message = f'SemanticError: {message}'
        if node is not None and hasattr(node, 'lineno') and node.lineno is not None:
            message += f' at line {node.lineno}'
        super().__init__(message)


class SemanticAnalyzer:

    def __init__(self):
        self.symbol_table = SymbolTable()


    def analyze(self, ast: Optional[Any]) -> Optional[Any]:
        if ast is None:
            return
        self.visit(ast)
        return ast


    def visit(self, node: Any) -> Optional[str]:
        print(f"Visiting node of type: {type(node).__name__}")  # Debugging print statement
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node: Any):
        raise SemanticError(f'No visit method for node type: {type(node).__name__}')


    def visit_ProgramDeclaration(self, node: ProgramDeclaration) -> Any:
        for decl in node.declarations:
            self.visit(decl)


    def visit_LemmaDeclaration(self, node: LemmaDeclaration) -> Any:
        # print(f"Visiting Lemma: {node.name}")
        self.visit(node.body)


    def visit_BodyDeclaration(self, node: BodyDeclaration) -> Any:
        # print(f"Visiting Body: {node.lineno}")
        self.visit(node.body)


    def visit_BinOpDeclaration(self, node: BinOpDeclaration) -> Any:
        # print(f"Visiting Binary Operation: {node.operation}")
        self.visit(node.left)
        self.visit(node.right)


    def visit_EVarDeclaration(self, node: EVarDeclaration) -> Any:
        # print(f"Visiting Variable: {node.name}")
        if not self.symbol_table.is_declared(node.name):
            self.symbol_table.add(node.name, node)
