from typing import Any

from servidor.utils.my_utils import split_expression

def apply_conjunction_introduction(
        logical_expr: str, # (p0 /\ p1)
        available_hypothesis: set[str], # []
        problem_id: str, #1
        auxiliar_formula : str
) -> list[dict[str, str | list[Any] | Any]]:

    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '∧':
        raise ValueError('conjunction introduction requires 3 arguments or symbol not ∧')

    antecedent, consequent = arguments[1], arguments[2]
    # print(f'{antecedent} -> {consequent}')

    result = [
        {
            "name": antecedent,
            "parentId": "",
            "child": [],
            "knowledge_base": [],
            "rule": "CI",
        },
        {
            "name": consequent,
            "parentId": "",
            "child": [],
            "knowledge_base": [],
            "rule": "CI",
        },
    ]

    return result