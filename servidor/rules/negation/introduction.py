from typing import Any

from servidor.utils.my_utils import split_expression
import re

def apply_negation_introduction(
        logical_expr: str, # (p0 /\ p1)
        available_hypothesis: set[str], # []
        problem_id: str, #1
        auxiliar_formula : str
) -> list[dict[str, str | list[Any] | Any]]:

    content = None
    match = re.search(r"EUnOp\(~, (.+)\)", logical_expr)

    if match:
        content = match.group(1)
    else: 
        raise ValueError("Logical expression must start with ~.")
        

    local_knowledge_base = {}
    tmp = f'X{problem_id}'
    local_knowledge_base[tmp] = content
    
    result = [
        {
            "name": "ABSURD_LITERAL",
            "parentId": "",
            "child": [],
            "knowledge_base": local_knowledge_base,

            # lamda wrong (just to test)
            "rule": "negation introduction",
        },
    ]

    return result