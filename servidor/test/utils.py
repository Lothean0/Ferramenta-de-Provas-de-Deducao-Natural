import re

from typing import List

from servidor.test.data_class import C_RED, C_END

def remove_outer_parentheses(s: str) -> str:

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

"""
This function checks if the antecedent or the negation of the consequent
is present in the knowledge base or wheter any of them can be deduced by
the current contents of the knowledge base.
"""
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
