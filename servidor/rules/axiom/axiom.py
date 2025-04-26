from typing import Any

from servidor.utils.my_utils import matches_any_order

def apply_axiom(
        logical_expr: str,
        available_hypothesis: set[tuple[str, Any]],  # Corrected type hint
        problem_id: str,
        auxiliar_formula: str
) -> list[dict[str, str | list[Any] | Any]]:

    available_hypothesis_dict = dict(available_hypothesis)

    try:
        if auxiliar_formula in available_hypothesis_dict:
            new_problem = available_hypothesis_dict[auxiliar_formula]
            print(f'THis is the problem{new_problem}')
            print(type(new_problem))

            if new_problem == logical_expr or matches_any_order(new_problem, logical_expr):
                result = [
                    {
                        "name": "",
                        "parentId": "",
                        "child": [],
                        "knowledge_base": [],
                    }
                ]

                return result

    except Exception as e:
        raise Exception(f"ERROR APPLYING AXIOM: {e}")
