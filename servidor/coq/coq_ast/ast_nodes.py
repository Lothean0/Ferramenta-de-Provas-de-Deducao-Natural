from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class ProgramDeclaration:
    declarations: List[Any]
    lineno: int


@dataclass
class ProofDeclaration:
    lineno: int


@dataclass
class LemmaDeclaration:
    name: str
    params: List[Any]
    body: Any
    lineno: int


@dataclass
class InstructionDeclaration:
    name: str
    params: str
    lineno: int


@dataclass
class QuitDeclaration:
    lineno: int


@dataclass
class EVarDeclaration:
    name: str
    lineno: int


@dataclass
class BodyDeclaration:
    body: Any
    lineno: int


@dataclass
class EUnOpDeclaration:
    operation: str
    name: Optional[EVarDeclaration]
    body: Optional[BodyDeclaration]
    lineno: int


@dataclass
class BinOpDeclaration:
    operation: str
    left: Any
    right: Any
    lineno: int

.\servidor\main.py .\servidor\test\data_class.py .\servidor\coq\coq_ast\ast_nodes.py .\servidor\coq\coq_parser\coq_lexer.py .\servidor\coq\coq_parser\coq_parser.py .\servidor\coq\coq_semantic\semantic_analyzer.py .\servidor\coq\coq_semantic\symbol_table.py .\servidor\dto\init__.py .\servidor\dto\logic_dto.py .\servidor\dto\user_dto.py .\servidor\test\truthtable.py
