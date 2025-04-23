from flask import Blueprint, request, jsonify
from servidor.app.utils.response_storage import response
from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer
from servidor.utils.my_utils import remove_outer_parentheses

from servidor.rules.implication.introduction import apply_implication_introduction
from servidor.rules.implication.elimination import apply_implication_elimination
from servidor.rules.axiom import apply_axiom


rules_bp = Blueprint("rules", __name__)

@rules_bp.route("/rules", methods=["POST"])
def apply_rules():
    try:
        data = request.get_json()
        print("Received data:", data)

        expression = data.get("expression")
        if not expression:
            return jsonify({"error": "Missing 'expression' parameter"}), 400

        print(data.get("knowledge_base"))

        # Parse the expression
        try:
            parsed_expression = CodeGenerator().generate_code(
                ast_2 := SemanticAnalyzer().analyze(
                    ast_1 := Parser.parse(expression, debug=False)
                )
            )
        except SyntaxError as e:
            return jsonify({"error": "Parsing failed", "details": str(e)}), 422

        print(f"Parsed Expression: {parsed_expression}")

        # Process the knowledge base
        knowledge_base_data = data.get("knowledge_base", [])
        knowledge_base_data_dict = {}

        if isinstance(knowledge_base_data, list):
            try:
                knowledge_base_data_dict = dict(knowledge_base_data)
            except (ValueError, TypeError) as e:
                return jsonify({
                    "error": "Invalid knowledge_base format",
                    "details": f"Expected list of key-value pairs. Error: {str(e)}"
                }), 400
        elif isinstance(knowledge_base_data, dict):
            knowledge_base_data_dict = knowledge_base_data
        else:
            return jsonify({
                "error": "Invalid knowledge_base format",
                "details": "Expected a list of key-value pairs or a dictionary."
            }), 400

        print(f"Type of knowledge_base: {type(data['knowledge_base'])}")
        print(f"Content of knowledge_base: {data['knowledge_base']}")

        try:
            if isinstance(knowledge_base_data_dict, dict):
                hypothesis_set = set(knowledge_base_data_dict.items())
            else:
                hypothesis_set = set()
        except Exception as e:
            return jsonify({
                "error": "Failed to process knowledge_base for hypothesis_set",
                "details": str(e)
            }), 400

        problem_id = data.get("id", "0")
        auxiliar_formula = data.get("auxiliar_formula", "")


        print(f"\n\nParsed expression: {parsed_expression}\n")
        print(f"Hypothesis set: {hypothesis_set}\n")
        print(f"Problem ID: {problem_id}\n")
        print(f"Auxiliar formula: {auxiliar_formula}\n")
        print(f"Rule: {data['rule']}\n")

        # Apply the rule
        try:
            rule_name = data.get("rule")
            function_name = 'apply_' + rule_name
            if function_name not in globals():
                return jsonify({"error": f"Rule function '{function_name}' not implemented"}), 400
            function = globals()[function_name]

            # 'expression': '(p0->p1)', 'rule': 'implication_introduction', 'knowledge_base': '[]', 'id': 1}
            result = function(parsed_expression, hypothesis_set, problem_id, auxiliar_formula)
            print(f'Worked')
            problem_id = int(problem_id)

            print(knowledge_base_data_dict)
            if not response:
                print("true")
                response.append({
                    "name": Parser.parse(parsed_expression),
                    "parentId": "",
                    "child": [],
                    "knowledge_base": knowledge_base_data_dict,
                })

            # Process the result list
            if isinstance(result, list):
                for _, item in enumerate(result, start=2):
                    knowledge_base_item = item.get("knowledge_base", {})

                    # Ensure knowledge_base_item is a dictionary
                    if isinstance(knowledge_base_item, list):
                        try:
                            knowledge_base_item = dict(knowledge_base_item)
                        except (ValueError, TypeError) as e:
                            return jsonify({
                                "error": "Invalid knowledge_base format in item",
                                 "details": f"Expected list of key-value pairs. Error: {str(e)}"
                            }), 400
                    elif not isinstance(knowledge_base_item, dict):
                        return jsonify({
                            "error": "Invalid knowledge_base format in item",
                            "details": "Expected a list of key-value pairs or a dictionary."
                    }), 400

                    # Merge the dictionaries
                    new_dict = {**knowledge_base_data_dict, **knowledge_base_item}
                    print(f"Merged knowledge_base: {new_dict}")

                    response.append({
                        "name": str(remove_outer_parentheses(Parser.parse(item.get("name")))),
                        "parentId": problem_id,
                        "child": [],
                        "knowledge_base": new_dict,
                    })



            print("Formatted Response:", response)
        except Exception as e:
            return jsonify({"error": "Function call failed", "details": str(e)}), 500

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500
