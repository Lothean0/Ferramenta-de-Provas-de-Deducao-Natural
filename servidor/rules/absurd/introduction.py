from typing import Any

def apply_RAA(
        logical_expr: str,
        available_hypothesis: set[str],
        problem_id: str,
        auxiliar_formula : str
) -> list[dict[str, str | list[Any] | Any]]:

    local_knowledge_base = {}
    tmp = f'X{problem_id}'
    local_knowledge_base[tmp] = f'EUnOp(~, {logical_expr})'
    
    result = [
        {
            "name": "ABSURD_LITERAL",
            "parentId": "",
            "child": [],
            "knowledge_base": local_knowledge_base,
            # lamda wrong (just to test)
            "lambda": "absurd introduction",
        },
    ]

    return result