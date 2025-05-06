"""
PARA AS REGRAS DE \\/ E <=> NAO ESTA A FUNCIONAR
PORQUE NAO SUBDIVIDI LAMBDA EM LEFT_TERM E RIGHT_TERM
"""

import json
import os
import logging
import re
import shutil
import sys
from uuid import uuid4, UUID
import signal

from anyio import value
from flask import Flask, jsonify, flash, request
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
# old
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
CORS(app, origins="*")

"""
THIS WORKS -> CLIENT BUILD new 
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

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def filter_recursive_children(parent_id):
    global response
    nodes_to_remove = set()

    def collect_descendants(node_id):
        for item in response:
            if item.get("parentId") == node_id:
                nodes_to_remove.add(item["uuid"])
                collect_descendants(item["uuid"])

    collect_descendants(parent_id)

    filtered_tree = [item for item in response if item["uuid"] not in nodes_to_remove]

    return filtered_tree


def process_tree(tree_data):
    for node in tree_data:
        name = node.get("name", "")
        parentId = node.get("parentId", "")
        knowledge_base = node.get("knowledge_base", {})
        child = node.get("child", [])
        uuid = node.get("uuid", None)

        global response
        response.append({
            "uuid" : uuid,
            "name": name,
            "parentId": parentId,
            "child": [],
            "knowledge_base": knowledge_base
        })

        # Recursively process child nodes if they exist
        if child:
            process_tree(child)
    print(response)



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
                local_knowledge_base[key] = item[1]
                local_counter += 1
        except Exception as e:
            return jsonify({"error": "Invalid knowledge_base format", "details": str(e)}), 400

        # print(local_knowledge_base)
        print(f'ADD NODE TYPE: {type(local_knowledge_base)}') # dict
        
        print(parsed_expression)
        print(Parser.parse(parsed_expression))
        bin_match = re.match(r'EBinOp\((.*?),', parsed_expression)
        un_match = re.match(r'EUnOp\((.*?),', parsed_expression)

        operator = None
        if bin_match:
            operator = bin_match.group(1)
        elif un_match:
            operator = un_match.group(1)
        print(operator)
        """
        thisdict = {
            "->": "λ x. {term}",
            "∨": "{side}( {term} )",
            "∧": "({side}( {term} ), {side}( {term} ))",
            "⟺": "({side}( {term} ), {side}( {term} ))",
            "~":" λ x. contradiction({x})"
        }
        """
        # O de baixo esta mal (foi so teste: o de cima deve estar certo)
        thisdict = {
            "->":"λ x. {term}",
            "∨": "{side}( {term} )",
            "∧":"({side}( {term} ), {side}( {term} ))",
            "⟺": "λ x. {term}",
            "~":"λ x. contradiction({x})"
        }
        lambda_value = thisdict.get(operator) if operator else "{term}"

        if not response:
            response.append({
                "uuid": uuid4(),
                "name": Parser.parse(parsed_expression),
                "parentId": "",
                "child": [],
                "knowledge_base": local_knowledge_base,
                "lambda": lambda_value
            })

        return jsonify(response), 200


    except Exception as e:
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500



@app.route("/api/rules", methods=["POST"])
def apply_rules():
    try:
        data = request.get_json()
        print("Received data:", data)

        print("THIS IS THE RESPONSE ARRAY BEFORE CHECKING PARENT_ID\n")
        #print()
        print("\nRESPONSE ARRAY FINISH")

        parent_id = data.get("id", "0")
        uuid = data.get("uuid", None)

        #if parent_id in processed_parent_ids:
         #   print("this id already was submitted to a rule")
          #  return jsonify({"error": f"Parent ID {parent_id} already processed"}), 400

        # processed_parent_ids.append(parent_id)

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

        auxiliar_formula = data.get("auxiliar_formula", "")

        print(f"\n\nUUID: {uuid}")
        print(f"Parsed expression: {parsed_expression}\n")
        print(f"Hypothesis set: {hypothesis_set}\n")
        print(f"Problem ID: {parent_id}\n")
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
            result = function(parsed_expression, hypothesis_set, parent_id, auxiliar_formula)
            print(f'Worked')
            problem_id = int(parent_id)

            print(knowledge_base_data_dict)

            global response
            print("ARRAY BEFORE FILER")
            print(response)
            response = filter_recursive_children(parent_id)
            print("ARRAY AFTER FILER")
            print(response)


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
                    new_dict = {
                        key : Parser.parse(val)
                        if isinstance(value, str) else val
                        for key, val in {**knowledge_base_data_dict, **knowledge_base_item}.items()
                    }

                    print(f"Merged knowledge_base: {new_dict}")

                    response.append({
                        "uuid" : uuid4(),
                        "name": str(remove_outer_parentheses(Parser.parse(item.get("name")))),
                        "parentId": problem_id,
                        "child": [],
                        "knowledge_base": new_dict,
                        "lambda": item.get("lambda"),
                    })

            print(f"Reponse starts here")
            print(response)

            # HERE WE NEED TO RECURSIVELY CHANGE THE PARENT LAMBDA TO THE CHILD ONE
            # RIGHT NOW ITS ONLY CHNAGING THE PARENT WITHOUT RECURSIVITY
            for entry in response:
                print(f"UUID: {entry.get('uuid')}")
                print(f"UUID IAM LOOKING FOR: {uuid}")
                if entry["uuid"] == UUID(uuid):
                    print(f"FOUND ENTRY: {entry}")

                    subgoal_term = None
                    for candidate in response:
                        if candidate.get("parentId") == parent_id:
                            subgoal_term = candidate.get("lambda")
                            break

                    if subgoal_term is None:
                        return jsonify({
                            "error": "Missing lambda term for subgoal",
                            "details": "Could not find matching subgoal term for substitution"
                        }), 400

                    entry["lambda"] = entry["lambda"].format(term=subgoal_term, side="left")
                    break

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


def cleanup_and_exit(signum, frame):
    temp_dirs = [UPLOAD_FOLDER, DOWNLOAD_FOLDER]

    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        print(f"Deleted folder: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        else:
            print(f"Directory not found: {temp_dir}")

    sys.exit(0)


signal.signal(signal.SIGINT, cleanup_and_exit)

if __name__ == "__main__":

    app.run(debug=True, port=3000)