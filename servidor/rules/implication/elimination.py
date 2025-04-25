from typing import Any

def apply_implication_elimination(
        logical_expr: str,
        available_hypothesis: set[tuple[str, Any]],  # Corrected type hint
        problem_id: str,
        auxiliar_formula: str
) -> list[dict[str, str | list[Any] | Any]]:

    available_hypothesis_dict = dict(available_hypothesis)

    try:
        if auxiliar_formula in available_hypothesis_dict:
            new_problem = available_hypothesis_dict[auxiliar_formula]

            result = [
                {
                    "name": f"EBinOp(->, {new_problem}, {logical_expr})",
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
        raise Exception(f"ERROR APPLYING IMPLICATION ELIMINATION: {e}")
