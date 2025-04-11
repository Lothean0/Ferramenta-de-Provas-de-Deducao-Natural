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
class ApplyRuleDeclaration:
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