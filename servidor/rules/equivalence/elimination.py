from typing import Any

from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer


def apply_equivalence_elimination_1(
        logical_expr: str,
        available_hypothesis: set[tuple[str, Any]],
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

        result = [
            {
                "name": f"EBinOp(⟺, {new_problem_parsed}, {logical_expr})",
                "parentId": "",
                "child": [],
                "knowledge_base": [],
                # lamda wrong (just to test)
                "lambda": "equivalence elimination",
            },
            {
                "name": new_problem_parsed,
                "parentId": "",
                "child": [],
                "knowledge_base": [],
                # lamda wrong (just to test)
                "lambda": "equivalence elimination",
            },
        ]

        return result


    except Exception as e:
        print(f"Exception in disjunction elimination: {e}")
        raise
    

def apply_equivalence_elimination_2(
        logical_expr: str,
        available_hypothesis: set[tuple[str, Any]],
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

        result = [
            {
                "name": f"EBinOp(⟺, {logical_expr}, {new_problem_parsed})",
                "parentId": "",
                "child": [],
                "knowledge_base": [],
            },
            {
                "name": new_problem_parsed,
                "parentId": "",
                "child": [],
                "knowledge_base": [],
            },
        ]

        return result


    except Exception as e:
        print(f"Exception in disjunction elimination: {e}")
        raise