import itertools
import re
from tabulate import tabulate

from servidor.test.data_class import *


def implication(
        a: bool,
        b: bool
) -> bool:
    return (not a) or b

def evaluate_expression(
        expr: str,
        values: dict
) -> bool:

    expr = "".join(expr.split())

    match = re.match(r"EVar\((p\d+)\)", expr)
    if match:
        return values[match.group(1)]

    match = re.match(r"EBinOp\((->),(.+),(.+)\)", expr)
    if match:
        left_expr = match.group(2)
        right_expr = match.group(3)
        return implication(evaluate_expression(left_expr, values), evaluate_expression(right_expr, values))

    raise ValueError(f"Invalid expression format: {expr}")

def generate_truth_table(
        logical_expr: str
) -> None:

    variables = sorted(set(re.findall(r"EVar\((.*?)\)", logical_expr)))
    # print(variables)

    table_data = []
    headers = variables + [logical_expr]

    for values in itertools.product([False, True], repeat=len(variables)):
        values_dict = dict(zip(variables, values))
        print(C_YELLOW + f'[DEBUG] ' +  C_END + f'{values_dict}')
        result = evaluate_expression(logical_expr, values_dict)
        print(C_GREEN + f'[INFO] ' + C_END + f'{logical_expr}: {result}\n')
        table_data.append([values_dict[var] for var in variables] + [result])

    # print(tabulate(table_data, headers=headers, tablefmt="grid"))

expression = input("Enter expression: ")  # Example: EBinOp(->, EVar(p0), EBinOp(->, EVar(p1), EVar(p2)))
generate_truth_table(expression)