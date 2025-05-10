from typing import Any

from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer
from servidor.utils.my_utils import matches_any_order

def apply_axiom(
        logical_expr: str,
        available_hypothesis: set[tuple[str, Any]],  # Corrected type hint
        problem_id: str,
        auxiliar_formula: str
) -> list[dict[str, str | list[Any] | Any]]:

    available_hypothesis_dict = dict(available_hypothesis)

    try:
        new_problem = available_hypothesis_dict.get(auxiliar_formula.upper(), auxiliar_formula)

        new_problem_parsed = CodeGenerator().generate_code(
            SemanticAnalyzer().analyze(
                Parser.parse(new_problem, debug=False)
            )
        )

        if matches_any_order(logical_expr, new_problem_parsed):
            print("Inisde")
            result = [
                {
                    "name": None,
                    "parentId": "",
                    "child": [],
                    "knowledge_base": [],
                    "lambda" : f"Axiom rule"
                }
            ]

            return result

    except Exception as e:
        print(f"Exception in disjunction elimination: {e}")
        raise
