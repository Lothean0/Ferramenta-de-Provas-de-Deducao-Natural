from typing import Any, Optional

from servidor.coq.coq_ast.ast_nodes import (
    ProgramDeclaration,
    LemmaDeclaration,
    ProofDeclaration,
    ApplyRuleDeclaration,
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


    def analyze(self, ast) -> Any:
        if ast is None:
            return

        self.visit(ast)
        return ast


    def visit(self, node: Any) -> Optional[str]:
        # print(f"Visiting node of type: {type(node).__name__}")  # Debugging print statement
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node: Any):
        raise SemanticError(f'No visit method for node type: {type(node).__name__}')


    def visit_ProgramDeclaration(self, node: ProgramDeclaration) -> Any:
        for decl in node.declarations:
            self.visit(decl)


    def visit_ProofDeclaration(self, node: ProofDeclaration) -> Any:
        print(f'[Visiting] ProofDeclaration\n')


    def visit_ApplyRuleDeclaration(self, node: ApplyRuleDeclaration) -> Any:
        print(f'[Visiting] ApplyRuleDeclaration\n')


    def visit_QuitDeclaration(self, node: QuitDeclaration) -> Any:
        print(f'[Visiting] QuitDeclaration\n')


    def visit_LemmaDeclaration(self, node: LemmaDeclaration) -> Any:
        # print(f"Visiting Lemma: {node.name}")
        for param in node.params:
            self.symbol_table.add(param["var_name"])
        print(f'Printing: {self.symbol_table}\n')
        self.visit(node.body)


    def visit_BodyDeclaration(self, node: BodyDeclaration) -> Any:
        # print(f"Visiting Body: {node.lineno}")
        print(f'This is the body:\n{node.body}\n')
        self.visit(node.body)

    def visit_BinOpDeclaration(self, node: BinOpDeclaration) -> Any:
        # print(f"Visiting Binary Operation: {node.operation}")
        # print(f'\n\nThis is a BinOpDeclaration:\n{node}')
        if node.operation not in ('→','∧','∨', '⟺'):
            raise SemanticError('Operation not supported')

        self.visit(node.left)
        self.visit(node.right)


    def visit_EVarDeclaration(self, node: EVarDeclaration) -> Any:
        # print(f"Visiting Variable: {node.name}")
        if not self.symbol_table.is_declared(node.name):
            raise SemanticError('Variable not declared')


    def visit_EUnOpDeclaration(self, node: EUnOpDeclaration) -> Any:
        if node.operation not in ('¬'):
            raise SemanticError('Operation not supported')

        if node.body is not None:
            self.visit(node.body)
