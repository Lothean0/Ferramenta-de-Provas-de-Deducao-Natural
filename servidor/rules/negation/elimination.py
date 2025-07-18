from typing import Any

from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer

def apply_negation_elimination(
        logical_expr: str,
        available_hypothesis: set[str],
        problem_id: str,
        auxiliar_formula : str
) -> list[dict[str, str | list[Any] | Any]]:

    if logical_expr != "ABSURD_LITERAL":
        raise ValueError("Logical expression must be ⊥")
    

    available_hypothesis_dict = dict(available_hypothesis)

    try:
        new_problem = available_hypothesis_dict.get(auxiliar_formula.upper(), auxiliar_formula)

        if not new_problem:
            raise ValueError("Auxiliary formula cannot be empty.")

        new_problem_parsed = CodeGenerator().generate_code(
            SemanticAnalyzer().analyze(
                Parser.parse(new_problem, debug=False)
            )
        )

        if not new_problem_parsed:
            raise ValueError("No new problem parsed.")

        result = [
            {
                "name": f"EUnOp(~,{new_problem_parsed})",
                "parentId": "",
                "child": [],
                "knowledge_base": [],
                "rule": "~E",
            },
            {
                "name": new_problem_parsed,
                "parentId": "",
                "child": [],
                "knowledge_base": [],
                "rule": "~E",
            },
        ]

        return result


    except Exception as e:
        print(f"Exception in negation elimination: {e}")
        raise