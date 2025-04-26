from typing import List, Optional
from servidor.config import *

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


def remove_outer_parentheses(s: str) -> Optional[str]:

    try:
        if not s.startswith('('):
            return s

        stack, result = [], []
        for char in s:
            stack.append(char)
            if stack.count('(') == stack.count(')'):
                result.append("".join(stack)[1:-1])
                stack = []

        return "".join(result)
    except Exception as e:
        return None



def split_expression(
        logical_expr: str,
) -> List[str]:
    pattern = r'([A-Za-z]+)\((.*)\)'
    match = re.match(pattern, logical_expr)
    if not match:
        raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Invalid expression')

    # match.group(1) = EbinOp
    content = match.group(2) # = [ -> , EVar(p0), EBinOp(->, EBinOp(->, EVar(p0), EVar(p1)), EVar(p1)) ]"
    balance, args, current_arg = 0, [], []

    for char in content:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1

        if char == ',' and balance == 0:
            args.append(''.join(current_arg).strip())
            current_arg = []
        else:
            current_arg.append(char)

    if current_arg:
        args.append(''.join(current_arg).strip())

    return args


import re

def parse_expr(s):
    s = s.strip()

    if s.startswith("EVar"):
        match = re.match(r"EVar\((\w+)\)", s)
        if match:
            return EVar(match.group(1))
        else:
            raise ValueError(f"Invalid EVar format: {s}")

    elif s.startswith("EBinOp"):
        s = s[6:].strip()
        if s[0] != '(':
            raise ValueError(f"Expected '(' after EBinOp: {s}")
        s = s[1:].strip()

        op_end = s.index(',')
        op = s[:op_end].strip()
        s = s[op_end + 1:].strip()

        left, rest = parse_until_comma(s)
        left = parse_expr(left.strip())

        right = parse_expr(rest.strip())

        return EBinOp(op, left, right)

    else:
        raise ValueError(f"Unknown expression format: {s}")


def parse_until_comma(s):
    depth = 0
    for i, c in enumerate(s):
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
        elif c == ',' and depth == 0:
            return s[:i], s[i + 1:]
    raise ValueError(f"Could not find comma at top level in {s}")


def equals_with_reordering(a, b):
    if isinstance(a, EVar) and isinstance(b, EVar):
        return a.name == b.name
    if isinstance(a, EBinOp) and isinstance(b, EBinOp):
        if a.op != b.op:
            return False
        if equals_with_reordering(a.left, b.left) and equals_with_reordering(a.right, b.right):
            return True
        if a.op in ['∧', '∨', '⟺']:
            if equals_with_reordering(a.left, b.right) and equals_with_reordering(a.right, b.left):
                return True
    return False


def matches_any_order(expr1_str, expr2_str):
    expr1 = parse_expr(expr1_str)
    expr2 = parse_expr(expr2_str)
    return equals_with_reordering(expr1, expr2)