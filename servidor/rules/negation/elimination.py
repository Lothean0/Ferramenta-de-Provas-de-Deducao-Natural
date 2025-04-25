from typing import Any

from servidor.utils.my_utils import split_expression
import re

def apply_negation_elimination(
        logical_expr: str, # (p0 /\ p1)
        available_hypothesis: set[str], # []
        problem_id: str, #1
        auxiliar_formula : str
) -> list[dict[str, str | list[Any] | Any]]:

    if logical_expr != "⊥":
        raise ValueError("Logical expression must be ⊥")
    

    available_hypothesis_dict = dict(available_hypothesis)

    try:
        if auxiliar_formula in available_hypothesis_dict:
            new_problem = available_hypothesis_dict[auxiliar_formula]

        result = [
            {
                "name": f"EUnOp(~,{new_problem})",
                "parentId": "",
                "child": [],
                "knowledge_base": [],
            },
            {
                "name": new_problem,
                "parentId": "",
                "child": [],
                "knowledge_base": [],
            },
        ]

        return result

    except Exception as e:
        raise Exception(f"ERROR APPLYING EQUIVALENCE ELIMINATION: {e}")