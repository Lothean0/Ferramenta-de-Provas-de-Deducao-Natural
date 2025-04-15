import ast
from typing import Any

from flask import Flask, jsonify
from flask_cors import CORS

from servidor.rules.implication.introduction import apply_implication_introduction
from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer


app = Flask(__name__)
CORS(app, origins="*")


@app.route("/api/result", methods=["GET"])
def validate_expression():

    request = {
        "id": 1,
        "expression": "p0->((p0->p1)->p1)",
        "rule": "implication_introduction",
        "knowledge_base": "[]",
        "child": [],
    }

    parsed_expression = CodeGenerator().generate_code(
        ast_2 := SemanticAnalyzer().analyze(
            ast_1 := Parser.parse(
                user_input := request['expression'], debug=False
            )
        )
    )

    request['expression'] = f"{parsed_expression}"
    print(request['expression'])

    try:
        hypothesis_list = ast.literal_eval(request["knowledge_base"])
        hypothesis_set = set(hypothesis_list) if isinstance(hypothesis_list, list) else set()
    except Exception as e:
        return jsonify({"error": "Invalid knowledge_base format", "details": str(e)}), 400

    problem_id = str(request["id"])

    try:
        function = globals()['apply_' + request['rule']]
        result = function(request['expression'], hypothesis_set, problem_id)
        print(f'Worked')

        response = []

        if not response:
            response.append({
                "name": Parser.parse(request["expression"]),
                "parentId": "",
                "child": [],
                "knowledge_base" : []
            })

        if isinstance(result, list):
            for item in result:
                if isinstance(item.get("name"), str):
                    item["name"] = Parser.parse(item.get("name"))
                if isinstance(item.get("parentId"), str):
                    item["parentId"] = request["id"]
            response.extend(result)
        else:
            if isinstance(result.get("name"), str):
                result["name"] = Parser.parse(result.get("name"))
            if isinstance(result.get("parentId"), str):
                result["parentId"] = request["id"]
            response.append(result)

    except Exception as e:
        return jsonify({"error": "Function call failed", "details": str(e)}), 500

    return jsonify(
        response
    ), 200





"""
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
    ]

    return jsonify(
        data
    ), 200
"""


if __name__ == "__main__":

    app.run(debug=True, port=3000)
