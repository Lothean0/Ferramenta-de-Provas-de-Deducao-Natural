import ast
import json

from typing import Any

from flask import Flask, jsonify
from flask_cors import CORS
from flask import request

from servidor.rules.implication.introduction import apply_implication_introduction
from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer


app = Flask(__name__)
CORS(app, origins="*")
# CORS(app, resources={r"/*": {"origins": "*"}})

"""
@app.route("/api/data", methods=["POST"])
def handle_post_data():
    try:
        # Parse the incoming JSON payload
        data = request.get_json()

        # Log the received data for debugging
        print("Received data:", data)

        # Example: Access specific fields from the payload
        expression = data.get("expression")
        rule = data.get("rule")
        knowledge_base = data.get("knowledge_base")

        # Perform any processing or validation here
        response = {
            "message": "Data received successfully",
            "received_expression": expression,
            "received_rule": rule,
            "received_knowledge_base": knowledge_base,
        }

        # Return a JSON response
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Failed to process data", "details": str(e)}), 400
"""

@app.route("/api/node", methods=["GET"])
def add_node():
    try:
        data = {
            "expression": request.args.get("expression"),
            "rule": request.args.get("rule"),
            "knowledge_base": request.args.get("knowledge_base"),
            "id": request.args.get("id"),
            "child": [],
        }


        if not data.get("expression"):
            return jsonify({"error": "Missing 'expression' parameter"}), 401

        # Parse the expression
        try:
            parsed_expression = CodeGenerator().generate_code(
                ast_2 := SemanticAnalyzer().analyze(
                    ast_1 := Parser.parse(data.get("expression"), debug=False)
                )
            )
        except SyntaxError as e:
            return jsonify({"error": "Parsing failed", "details": str(e)}), 501

        # Process the knowledge base

        if not response:
            response.append({
                "name": Parser.parse(parsed_expression),
                "parentId": "",
                "child": [],
                "knowledge_base": request.args.get("knowledge_base", "[]"),
            })

        return jsonify(response), 200


    except Exception as e:
        return jsonify({"error": "Failed to process request", "details": str(e)}), 503

@app.route("/api/result", methods=["GET"])
def validate_expression():
    try:
        # Retrieve the expression from the request

        expression = request.args.get("expression")
        if not expression:
            return jsonify({"error": "Missing 'expression' parameter"}), 401

        print(request.args.get("knowledge_base"))

        # Parse the expression
        try:
            parsed_expression = CodeGenerator().generate_code(
                ast_2 := SemanticAnalyzer().analyze(
                    ast_1 := Parser.parse(expression, debug=False)
                )
            )
        except SyntaxError as e:
            return jsonify({"error": "Parsing failed", "details": str(e)}), 501

        print(f"{parsed_expression}")

        # Process the knowledge base
        try:
            hypothesis_list = ast.literal_eval(request.args.get("knowledge_base", "[]"))
            hypothesis_set = set(hypothesis_list) if isinstance(hypothesis_list, list) else set()
        except Exception as e:
            return jsonify({"error": "Invalid knowledge_base format", "details": str(e)}), 402

        problem_id = request.args.get("id", "0")

        # Apply the rule
        try:
            function = globals()['apply_' + request.args.get("rule")]
            result = function(parsed_expression, hypothesis_set, problem_id)
            print(f'Worked')
            problem_id = int(problem_id)

            if not response:
                response.append({
                    "name": Parser.parse(parsed_expression),
                    "parentId": "",
                    "child": [],
                    "knowledge_base": request.args.get("knowledge_base", "[]"),
                })


            if isinstance(result, list):
                for _,item in enumerate(result, start=2):
                    response.append({
                        "name": str(Parser.parse(item.get("name"))),
                        "parentId": problem_id,
                        "child": [],
                        "knowledge_base": item.get("knowledge_base", [])
                    })
            else:
                response.append({
                    "name": str(Parser.parse(result.get("name"))),
                    "parentId": problem_id,
                    "child": [],
                    "knowledge_base": result.get("knowledge_base", [])
                })

            print("Formatted Response:", response)
        except Exception as e:
            return jsonify({"error": "Function call failed", "details": str(e)}), 502

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Failed to process request", "details": str(e)}), 503





@app.route("/api/teste", methods=["GET"])
def send_data():

    data = [
        {
            "name": "p0->((p0->p1)->p1)",
            "parentId": "",
            "child": []
        },
        {
            "name": "(p0->p1)->p1",
            "parentId": 1,
            "child": []
        },
        {
            "name": "p1",
            "parentId": 2,
            "child": []
        },
        {
            "name": "p0",
            "parentId": 3,
            "child": []
        },
        {
            "name": "p0->p1",
            "parentId": 3,
            "child": []
        },
        {
            "name": "p0->p1->p12333",
            "parentId": 3,
            "child": []
        },
    ]

    return jsonify(
        data
    ), 200


if __name__ == "__main__":

    response = []

    app.run(debug=True, port=3000)
