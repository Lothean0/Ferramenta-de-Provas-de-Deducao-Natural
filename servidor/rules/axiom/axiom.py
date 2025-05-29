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
        print(f"This is the aux formula: {auxiliar_formula}")
        new_problem = available_hypothesis_dict.get(auxiliar_formula.upper(), auxiliar_formula)

        print(list(available_hypothesis_dict.values()))
        if new_problem not in list(available_hypothesis_dict.values()):
            raise ValueError(f"Auxiliary formula '{auxiliar_formula}' not found in available hypotheses.")
        
        new_problem_parsed = CodeGenerator().generate_code(
            SemanticAnalyzer().analyze(
                Parser.parse(new_problem, debug=False)
            )
        )

        print(f"Thi is the parsed_problem: {new_problem_parsed}")
        print(f"this is the logical expression: {logical_expr}")
        print(f"Type of both = {type(new_problem_parsed)} and {type(logical_expr)}")

        if not new_problem_parsed:
            raise ValueError("Auxiliary formula cannot be empty.")

        """
        prefix = "EUnOp(~,"
        if logical_expr.startswith(prefix):
            result1 = logical_expr[len(prefix):].strip()

            if result1.endswith(")"):
                logical_expr = result1[:-1].strip()

        if new_problem_parsed.startswith("EUnOp(~,"):

            prefix = "EUnOp(~,"
            if new_problem_parsed.startswith(prefix):
                result2 = new_problem_parsed[len(prefix):].strip()

                if result2.endswith(")"):
                    new_problem_parsed = result2[:-1].strip()
        """

        if logical_expr == new_problem_parsed:
            print("Inisde")
            result = [
                {
                    "name": None,
                    "parentId": "",
                    "child": [],
                    "knowledge_base": [],
                    "rule" : f"{auxiliar_formula.upper()}"
                }
            ]

            return result

    except Exception as e:
        print(f"Exception in axiom: {e}")
        raise


