from typing import Any, Optional


class SymbolTable:

    def __init__(self):
        self.symbols = {}

    def add(self, name: str, declaration: Any):
        self.symbols[name] = declaration

    def lookup(self, name: str) -> Optional[Any]:
        return self.symbols.get(name, None)

    def is_declared(self, name: str) -> bool:
        return name in self.symbols
