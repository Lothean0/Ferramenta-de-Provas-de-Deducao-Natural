from typing import Any

def apply_axiom(
        logical_expr: str,
        available_hypothesis: set[tuple[str, Any]],  # Corrected type hint
        problem_id: str,
        auxiliar_formula: str
) -> list[dict[str, str | list[Any] | Any]]:

    available_hypothesis_dict = dict(available_hypothesis)
    print("got inside axiom")

    try:
        if auxiliar_formula in available_hypothesis_dict:
            new_problem = available_hypothesis_dict[auxiliar_formula]
            if new_problem == logical_expr:
                result = []

                return result

    except Exception as e:
        raise Exception(f"ERROR APPLYING AXIOM: {e}")
