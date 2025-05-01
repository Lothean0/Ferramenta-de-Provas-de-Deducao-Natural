import json
import os
import logging
from uuid import uuid4
from flask import Flask, jsonify, request, flash
from flask_cors import CORS
from werkzeug.utils import secure_filename

from servidor.rules.axiom import apply_axiom
from servidor.rules.implication.introduction import apply_implication_introduction
from servidor.rules.implication.elimination import apply_implication_elimination
from servidor.rules.conjunction.introduction import apply_conjunction_introduction
from servidor.rules.conjunction.elimination import apply_conjunction_elimination_1, apply_conjunction_elimination_2
from servidor.rules.disjunction.introduction import apply_disjunction_introduction_1, apply_disjunction_introduction_2
from servidor.rules.disjunction.elimination import apply_disjunction_elimination
from servidor.rules.negation.introduction import apply_negation_introduction
from servidor.rules.negation.elimination import apply_negation_elimination
from servidor.rules.equivalence.introduction import apply_equivalence_introduction
from servidor.rules.equivalence.elimination import apply_equivalence_elimination_1, apply_equivalence_elimination_2
from servidor.rules.absurd.introduction import apply_RAA
from servidor.rules.absurd.elimination import apply_absurd_elimination

from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer
from servidor.utils.my_utils import remove_outer_parentheses

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'json'}

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
CORS(app, origins="*")

response_data = []
counter = 0


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def filter_descendants(parent_id):
    nodes_to_remove = set()

    def collect(node_id):
        for item in response_data:
            if item.get("parentId") == node_id:
                nodes_to_remove.add(item["uuid"])
                collect(item["uuid"])

    collect(parent_id)
    return [item for item in response_data if item["uuid"] not in nodes_to_remove]


@app.route("/api/node", methods=["POST"])
def add_node():
    if response_data:
        return jsonify({"error": "Reset first", "details": str(response_data)}), 400

    data = request.get_json()
    expr = data.get("expression")
    if not expr:
        return jsonify({"error": "Missing 'expression' parameter"}), 400

    try:
        parsed_expression = CodeGenerator().generate_code(
            SemanticAnalyzer().analyze(Parser.parse(expr, debug=False))
        )
    except SyntaxError as e:
        return jsonify({"error": "Parsing failed", "details": str(e)}), 422

    local_kb = {}
    try:
        for idx, item in enumerate(data.get("knowledge_base", []), start=1):
            key = f"Y{idx}"
            parsed_kb_expr = CodeGenerator().generate_code(
                SemanticAnalyzer().analyze(Parser.parse(item[1], debug=False))
            )
            local_kb[key] = parsed_kb_expr
    except Exception as e:
        return jsonify({"error": "Invalid knowledge_base format", "details": str(e)}), 400

    response_data.append({
        "uuid": uuid4(),
        "name": Parser.parse(parsed_expression),
        "parentId": "",
        "child": [],
        "knowledge_base": local_kb
    })
    return jsonify(response_data), 200


@app.route("/api/rules", methods=["POST"])
def apply_rules():
    data = request.get_json()
    expr = data.get("expression")
    parent_id = data.get("id")
    uuid = data.get("uuid")
    auxiliar_formula = data.get("auxiliar_formula", "")
    rule_name = data.get("rule")

    if not expr or not rule_name:
        return jsonify({"error": "Missing 'expression' or 'rule' parameter"}), 400

    try:
        parsed_expr = CodeGenerator().generate_code(
            SemanticAnalyzer().analyze(Parser.parse(expr, debug=False))
        )
    except SyntaxError as e:
        return jsonify({"error": "Parsing failed", "details": str(e)}), 422

    kb_data = data.get("knowledge_base", [])
    try:
        kb_dict = dict(kb_data) if isinstance(kb_data, list) else kb_data
        hypothesis_set = set(kb_dict.items())
    except Exception as e:
        return jsonify({"error": "Invalid knowledge_base format", "details": str(e)}), 400

    try:
        function = globals().get(f'apply_{rule_name}')
        if not function:
            return jsonify({"error": f"Rule function 'apply_{rule_name}' not implemented"}), 400

        result = function(parsed_expr, hypothesis_set, parent_id, auxiliar_formula)
        global response_data
        response_data = filter_descendants(parent_id)

        for item in result:
            item_kb = item.get("knowledge_base", {})
            if isinstance(item_kb, list):
                item_kb = dict(item_kb)

            merged_kb = {**kb_dict, **item_kb}
            response_data.append({
                "uuid": uuid4(),
                "name": str(remove_outer_parentheses(Parser.parse(item.get("name")))),
                "parentId": int(parent_id),
                "child": [],
                "knowledge_base": merged_kb,
            })

    except Exception as e:
        return jsonify({"error": "Function call failed", "details": str(e)}), 500

    return jsonify(response_data), 200


@app.route("/api/reset", methods=["POST"])
def reset_data():
    response_data.clear()
    return jsonify(response_data), 200


@app.route("/api/save", methods=["POST"])
def save_file():
    global counter
    data = request.get_json()
    counter += 1
    filename = f'tree-data-{counter}.json'

    if not allowed_file(filename):
        return jsonify({"error": "Invalid file type"}), 400

    try:
        with open(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), 'w') as f:
            json.dump(data, f, indent=2)
        return jsonify({"message": "Data saved to file successfully!", "number": counter}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/file", methods=["POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        # If ithe user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return jsonify({"error": "No file part"}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as file:
                treedata = file.read()

                print("Debug - treedata:", treedata)
                treedata_json = json.loads(treedata)
                process_tree(treedata_json["tree"])

            return jsonify({"filename": treedata}), 200

    return jsonify({"error": "File not allowed"}), 400


def process_tree(tree):
    for node in tree:
        response_data.append({
            "uuid": node.get("uuid"),
            "name": node.get("name"),
            "parentId": node.get("parentId"),
            "child": [],
            "knowledge_base": node.get("knowledge_base", {})
        })
        if node.get("child"):
            process_tree(node.get("child"))


if __name__ == "__main__":
    app.run(debug=True, port=3000)
