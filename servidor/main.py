import json
import os

from flask import Flask, jsonify, flash, redirect, url_for, send_from_directory
from flask_cors import CORS
from flask import request
from werkzeug.utils import secure_filename

from servidor.rules.implication.introduction import apply_implication_introduction
from servidor.propositional_logic.propositional_logic_codegen import CodeGenerator
from servidor.propositional_logic.propositional_logic_parser import Parser
from servidor.propositional_logic.propositional_logic_semantic import SemanticAnalyzer


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
CORS(app, origins="*")

# CORS(app, resources={r"/*": {"origins": "*"}})

response = []

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

@app.route("/api/node", methods=["POST"])
def add_node():
    try:
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

        # Process the knowledge base

        if not response:
            response.append({
                "name": Parser.parse(parsed_expression),
                "parentId": "",
                "child": [],
                "knowledge_base": data.get("knowledge_base", "[]"),
            })

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

        print(f"{parsed_expression}")

        # Process the knowledge base
        try:
            hypothesis_set = set(data["knowledge_base"]) if isinstance(data["knowledge_base"], list) else set()
        except Exception as e:
            return jsonify({"error": "Invalid knowledge_base format", "details": str(e)}), 400

        problem_id = data.get("id", "0")

        # Apply the rule
        try:
            function = globals()['apply_' + data.get("rule")]
            # 'expression': '(p0->p1)', 'rule': 'implication_introduction', 'knowledge_base': '[]', 'id': 1}
            result = function(parsed_expression, hypothesis_set, problem_id)
            print(f'Worked')
            problem_id = int(problem_id)

            if not response:
                response.append({
                    "name": Parser.parse(parsed_expression),
                    "parentId": "",
                    "child": [],
                    "knowledge_base": data.get("knowledge_base", "[]"),
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
    data = request.get_json()  # Get the data from the request
    print("Received data:", data)

    # Define the path where the file will be saved
    file_path = 'tree_structure.txt'

    # Convert the received data into a string format
    tree_data_str = json.dumps(data, indent=2)  # Pretty-print the JSON data

    # Write the string data to a .txt file
    try:
        with open(file_path, 'w') as file:
            file.write(tree_data_str)
        return jsonify({"message": "Data saved to file successfully!"}), 200
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
        # If the user does not select a file, the browser submits an
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


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

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
