import ast

from flask import Flask, jsonify
from flask_cors import CORS
from rules.implication.introduction import apply_implication_introduction

app = Flask(__name__)
CORS(app, origins="*")


@app.route("/api/teste", methods=["GET"])
def validate_expression():

    # ver os tipos (str, set[str], ... )
    data = {
        "id": 1,
        "expression": "EBinOp(->, EVar(p0), EVar(p2))",
        "rule": "implication_introduction",
        "knowledge_base": "[]"
    }

    try:
        hypothesis_list = ast.literal_eval(data["knowledge_base"])
        hypothesis_set = set(hypothesis_list) if isinstance(hypothesis_list, list) else set()
    except Exception as e:
        return jsonify({"error": "Invalid knowledge_base format", "details": str(e)}), 400

    problem_id = str(data["id"])

    try:
        function = globals()['apply_' + data['rule']]
        result = function(data['expression'], hypothesis_set, problem_id)
        print(f'Worked')

        # the result of applying a rule must be in this form (or similar)
        """result = {
            "id" : 2,
            "expression": "EVar(p1))",
            "knowledge_base": "X0: EVar(p1)",
        }
        """


    except Exception as e:
        return jsonify({"error": "Function call failed", "details": str(e)}), 500

    return jsonify({
        "knowledge_base": hypothesis_list,
        "result": result,
    }), 600


if __name__ == "__main__":

    app.run(debug=True, port=3000)
