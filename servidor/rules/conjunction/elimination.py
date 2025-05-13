from typing import Any

from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer


def apply_conjunction_elimination_1(
        logical_expr: str,
        available_hypothesis: set[tuple[str, Any]],  # Corrected type hint
        problem_id: str,
        auxiliar_formula: str
) -> list[dict[str, str | list[Any] | Any]]:
    available_hypothesis_dict = dict(available_hypothesis)

    try:
        new_problem = available_hypothesis_dict.get(auxiliar_formula.upper(), auxiliar_formula)
        # Check if the logical expression is in the form of a conjunction
        if not new_problem:
            raise ValueError("Auxiliary formula cannot be empty.")
    
        new_problem_parsed = CodeGenerator().generate_code(
            SemanticAnalyzer().analyze(
                Parser.parse(new_problem, debug=False)
            )
        )


        result = [
            {
                "name": f"EBinOp(∧, {new_problem_parsed}, {logical_expr})",
                "parentId": "",
                "child": [],
                "knowledge_base": [],
                "lambda": "conjunction elimination",
            },
        ]

        return result


    except Exception as e:
        print(f"Exception in disjunction elimination: {e}")
        raise


def apply_conjunction_elimination_2(
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

        if not new_problem_parsed:
            raise ValueError("Auxiliary formula cannot be empty.")

        result = [
            {
                "name": f"EBinOp(∧, {logical_expr}, {new_problem_parsed})",
                "parentId": "",
                "child": [],
                "knowledge_base": [],
                # lamda wrong (just to test)
                "lambda": "conjunction elimination",
            }
        ]

        return result


    except Exception as e:
        print(f"Exception in disjunction elimination: {e}")
        raise
