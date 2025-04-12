import ast

from flask import Flask, jsonify
from flask_cors import CORS

from rules.implication.introduction import apply_implication_introduction
from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer


app = Flask(__name__)
CORS(app, origins="*")


@app.route("/api/teste", methods=["GET"])
def validate_expression():

    # ver os tipos (str, set[str], ... )
    data = {
        "id": 1,
        "expression": "p1 -> p2",
        "rule": "implication_introduction",
        "knowledge_base": "[]"
    }

    parsed_expression = CodeGenerator().generate_code(ast_2 := SemanticAnalyzer().analyze(ast_1 := Parser.parse(user_input := data['expression'], debug=False)))
    data['expression'] = f"{parsed_expression}"
    print(data['expression'])

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
