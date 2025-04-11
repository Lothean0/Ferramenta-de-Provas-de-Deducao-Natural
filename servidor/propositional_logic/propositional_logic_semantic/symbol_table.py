class SymbolTable:

    def __init__(self):
        self.symbols = []


    def add(self, name: str):
        self.symbols.append(name)


    def is_declared(self, name: str) -> bool:
        return name in self.symbols


    def __str__(self):
        return f'Symbol table: {self.symbols}'