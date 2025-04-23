from flask import Blueprint, request, jsonify
from servidor.app.utils.response_storage import response
from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer

node_bp = Blueprint("node", __name__)


@node_bp.route("/node", methods=["POST"])
def add_node():
    try:
        local_counter = 1
        local_knowledge_base = {}
        if response:
            return jsonify({"error": "Reset first", "details": str(response)}), 400

        data = request.get_json()
        print("Received data:", data)

        if not data.get("expression"):
            # print("No expression provided")
            return jsonify({"error": "Missing 'expression' parameter"}), 400

        # Parse the expression
        try:
            parsed_expression = CodeGenerator().generate_code(
                ast_2 := SemanticAnalyzer().analyze(
                    ast_1 := Parser.parse(data.get("expression"), debug=False)
                )
            )
        except SyntaxError as e:
            return jsonify({"error": "Parsing failed", "details": str(e)}), 422

        print("Here_1")

        try:
            for item in data.get("knowledge_base", []):
                print(item[1])
                key = f"Y{local_counter}"
                parsed_expr = CodeGenerator().generate_code(
                    ast_2 := SemanticAnalyzer().analyze(
                        ast_1 := Parser.parse(item[1], debug=False)
                    )
                )
                local_knowledge_base[key] = parsed_expr
                local_counter += 1
        except Exception as e:
            return jsonify({"error": "Invalid knowledge_base format", "details": str(e)}), 400

        # print(local_knowledge_base)
        print(f'ADD NODE TYPE: {type(local_knowledge_base)}')  # dict

        if not response:
            response.append({
                "name": Parser.parse(parsed_expression),
                "parentId": "",
                "child": [],
                "knowledge_base": local_knowledge_base
            })

        print("Here_3")

        return jsonify(response), 200


    except Exception as e:
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500
