from attr import dataclass
from typing import Any, List, Optional, Dict

@dataclass
class Expression:
    name: str
    expression: str
    value: Optional[bool]
    lineno: int