C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_BLUE = '\033[94m'
C_END = '\033[0m'

class EVar:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"EVar({self.name})"


class EBinOp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"EBinOp('{self.op}', {self.left}, {self.right})"