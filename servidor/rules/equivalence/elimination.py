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
        if auxiliar_formula in available_hypothesis_dict:
            new_problem = CodeGenerator().generate_code(
                SemanticAnalyzer().analyze(
                    Parser.parse(available_hypothesis_dict[auxiliar_formula], debug=False)
                )
            )

            result = [
                {
                    "name": f"EBinOp(⟺, {new_problem}, {logical_expr})",
                    "parentId": "",
                    "child": [],
                    "knowledge_base": [],
                    # lamda wrong (just to test)
                    "lambda": "equivalence elimination",
                },
                {
                    "name": new_problem,
                    "parentId": "",
                    "child": [],
                    "knowledge_base": [],
                    # lamda wrong (just to test)
                    "lambda": "equivalence elimination",
                },
            ]

            return result

    except Exception as e:
        raise Exception(f"ERROR APPLYING EQUIVALENCE ELIMINATION: {e}")
    

def apply_equivalence_elimination_2(
        logical_expr: str,
        available_hypothesis: set[tuple[str, Any]],
        problem_id: str,
        auxiliar_formula: str
) -> list[dict[str, str | list[Any] | Any]]:

    available_hypothesis_dict = dict(available_hypothesis)

    try:
        if auxiliar_formula in available_hypothesis_dict:
            new_problem = available_hypothesis_dict[auxiliar_formula]

            result = [
                {
                    "name": f"EBinOp(⟺, {logical_expr}, {new_problem})",
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