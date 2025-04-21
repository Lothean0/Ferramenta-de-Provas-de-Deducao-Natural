import json
import os

from flask import Flask, jsonify, flash, redirect, url_for, send_from_directory
from flask_cors import CORS
from flask import request
from networkx.algorithms.lowest_common_ancestors import lowest_common_ancestor
from werkzeug.utils import secure_filename

from servidor.config import knowledge_base
from servidor.rules.implication.introduction import apply_implication_introduction
from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer


UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'json'}

# old
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
CORS(app, origins="*")

"""
new 
app = Flask(__name__, static_folder='dist')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
CORS(app, origins="*")

@app.route('/')
def index():
    return send_from_directory('dist', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('dist', path)
"""

response = []
counter = 0

@app.route("/api/node", methods=["POST"])
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
        print(f'ADD NODE TYPE: {type(local_knowledge_base)}') # dict

        if not response:
            response.append({
                "name": Parser.parse(parsed_expression),
                "parentId": "",
                "child": [],
                "knowledge_base": local_knowledge_base
            })

        """
        knowledge_base: {Y1: 'p0'}
        knowledge_base:
            Y1: "p0"
          > [[Prototype]] : Obejct
          
          
          
        knowledge_base: {X0: 'EVar(p0)'}
        knoledge_base:
            X0: EVar(p0)
            > [[Prototype]] : Obejct
        """

        print("Here_3")

        return jsonify(response), 200


    except Exception as e:
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500

@app.route("/api/rules", methods=["POST"])
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

        # Convert knowledge_base_data to a set of tuples for hypothesis_set
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

        # Apply the rule
        try:
            function = globals()['apply_' + data.get("rule")]
            # 'expression': '(p0->p1)', 'rule': 'implication_introduction', 'knowledge_base': '[]', 'id': 1}
            result = function(parsed_expression, hypothesis_set, problem_id)
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
                        "name": str(Parser.parse(item.get("name"))),
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


@app.route("/api/reset", methods=["POST"])
def reset_data():
    print("Reseting data ...")
    response.clear()
    return jsonify(response), 200

@app.route("/api/save", methods=["POST"])
def save_file():
    data = request.get_json()
    print("Received data:", data)

    global counter
    counter += 1

    filename = f'tree-data-{counter}.json'

    if not allowed_file(filename):
        return jsonify({"error": "Invalid file type"}), 400

    tree_data_str = json.dumps(data, indent=2)

    try:
        with open(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), 'w') as file:
            file.writelines(tree_data_str)

        return jsonify(
            {"message": "Data saved to file successfully!",
             "number": counter
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            return jsonify({"filename": treedata}), 200

    return jsonify({"error": "File not allowed"}), 400




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

    app.run(debug=True, port=3000)
