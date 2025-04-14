import ast

from flask import Flask, jsonify
from flask_cors import CORS

from rules.implication.introduction import apply_implication_introduction
from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer


app = Flask(__name__)
CORS(app, origins="*")


@app.route("/api/rule_result", methods=["GET"])
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
                "child": []
            })

        if isinstance(result, list):
            response.extend(result)
        else:
            response.append(result)

        """
        result_expression_1 = "(p0->p1)->p1"
        result_expression_2 = "p1",
        result_expression_3 = "p0",
        result_expression_4 = "p0->p1",


        response.append({
            "name": result_expression_1,
            "parentId": request["id"],
            "child": []
        })

        response.append({
            "name": result_expression_2,
            "parentId": 2,
            "child": []
        })

        response.append({
            "name": result_expression_3,
            "parentId": 3,
            "child": []
        })

        response.append({
            "name": result_expression_4,
            "parentId": 3,
            "child": []
        })
        """

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
