from typing import Any

from servidor.utils.my_utils import split_expression

def apply_disjunction_elimination(
        logical_expr: str,
        available_hypothesis: set[tuple[str, Any]],
        problem_id: str,
        auxiliar_formula: str
) -> list[dict[str, str | list[Any] | Any]]:

    available_hypothesis_dict = dict(available_hypothesis)

    try:
        if auxiliar_formula in available_hypothesis_dict:
            new_problem = available_hypothesis_dict[auxiliar_formula]

            arguments = split_expression(new_problem)

            if len(arguments) != 3 or arguments[0] != '∨':
                raise ValueError('Disjunction elimination requires 3 arguments or symbol not ∨')
            
            antecedent, consequent = arguments[1], arguments[2]
            local_knowledge_base1 = {}
            tmp = f'X{problem_id}'
            local_knowledge_base1[tmp] = antecedent

            local_knowledge_base2 = {}
            tmp = f'Z{problem_id}'
            local_knowledge_base2[tmp] = consequent

            result = [
                {
                    "name": new_problem,
                    "parentId": "",
                    "child": [],
                    "knowledge_base": [],
                },
                {
                    "name": logical_expr,
                    "parentId": "",
                    "child": [],
                    "knowledge_base": local_knowledge_base1,
                },
                {
                    "name": logical_expr,
                    "parentId": "",
                    "child": [],
                    "knowledge_base": local_knowledge_base2,
                },
            ]
            return result

    except Exception as e:
        raise Exception(f"ERROR APPLYING EQUIVALENCE ELIMINATION: {e}")