from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class ProgramDeclaration:
    declarations: List[Any]
    lineno: int


@dataclass
class EVarDeclaration:
    name: str
    lineno: int


@dataclass
class ExpressionDeclaration:
    body: Any
    lineno: int


@dataclass
class EUnOpDeclaration:
    operation: str
    name: Optional[EVarDeclaration]
    body: Optional[ExpressionDeclaration]
    lineno: int


@dataclass
class BinOpDeclaration:
    operation: str
    left: Any
    right: Any
    lineno: int