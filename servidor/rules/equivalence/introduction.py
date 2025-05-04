from typing import Any

from servidor.utils.my_utils import split_expression

def apply_equivalence_introduction(
        logical_expr: str, # (p0 <-> p1)
        available_hypothesis: set[str],
        problem_id: str,
        auxiliar_formula : str
) -> list[dict[str, str | list[Any] | Any]]:
    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '⟺':
        raise ValueError('equivalence introduction requires 3 arguments or symbol not ⟺')

    antecedent, consequent = arguments[1], arguments[2]
    local_knowledge_base1 = {}
    tmp = f'X{problem_id}'
    local_knowledge_base1[tmp] = antecedent

    local_knowledge_base2 = {}
    tmp = f'Z{problem_id}'
    local_knowledge_base2[tmp] = consequent

    result = [
        {
            "name": consequent,
            "parentId": "",
            "child": [],
            "knowledge_base": local_knowledge_base1,
            # lamda wrong (just to test)
            "lambda": "equivalence introduction",
        },
        {
            "name": antecedent,
            "parentId": "",
            "child": [],
            "knowledge_base": local_knowledge_base2,
            # lamda wrong (just to test)
            "lambda": "equivalence introduction",
        },
    ]

    return result