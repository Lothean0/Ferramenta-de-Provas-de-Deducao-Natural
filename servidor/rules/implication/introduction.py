from typing import Any

from servidor.utils.my_utils import split_expression

def apply_implication_introduction(
        logical_expr: str, # (p0 ->p1)
        available_hypothesis: set[str], # []
        problem: str #1
) -> list[dict[str, str | list[Any] | Any]]:

    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '->':
        raise ValueError('Implication introduction requires 3 arguments or symbol not ->')

    antecedent, consequent = arguments[1], arguments[2]
    # print(f'{antecedent} -> {consequent}')

    local_knowledge_base = {}
    tmp = f'X{problem}'
    local_knowledge_base[tmp] = antecedent

    result = [
        {
            "name": consequent,
            "parentId": "",
            "child": [],
            "knowledge_base": local_knowledge_base,
        },
    ]

    return result