from typing import Any

from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer
from servidor.utils.my_utils import split_expression

def apply_disjunction_elimination(
        logical_expr: str,
        available_hypothesis: set[tuple[str, Any]],
        problem_id: str,
        auxiliar_formula: str
) -> list[dict[str, str | list[Any] | Any]]:

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

        print(f"Parsed_expression_inside_elimination: {new_problem_parsed}")
        
        if not new_problem_parsed:
            raise ValueError('Disjunction elimination requires 3 arguments or symbol not ∨')
        arguments = split_expression(new_problem_parsed)

        if len(arguments) != 3 or arguments[0] != '∨':
            raise ValueError('Disjunction elimination requires 3 arguments or symbol not ∨')
            
        antecedent, consequent = arguments[1], arguments[2]
        local_knowledge_base1 = {}
        tmp = f'X{problem_id}'
        local_knowledge_base1[tmp] = antecedent

        local_knowledge_base2 = {}
        tmp = f'Z{problem_id}'
        local_knowledge_base2[tmp] = consequent

        print(f"{tmp}:{antecedent}")
        print(f"{tmp}:{consequent}")

        result = [
            {
                "name": new_problem_parsed,
                "parentId": "",
                "child": [],
                "knowledge_base": [],
                # lamda wrong (just to test)
                "lambda": "disjunction elimination",
            },
            {
                "name": logical_expr,
                "parentId": "",
                "child": [],
                "knowledge_base": local_knowledge_base1,
                # lamda wrong (just to test)
                "lambda": "disjunction elimination",
            },
            {
                "name": logical_expr,
                "parentId": "",
                "child": [],
                "knowledge_base": local_knowledge_base2,
                # lamda wrong (just to test)
                "lambda": "disjunction elimination",
            },
        ]

        return result

    except Exception as e:
        print(f"Exception in disjunction elimination: {e}")
        raise
