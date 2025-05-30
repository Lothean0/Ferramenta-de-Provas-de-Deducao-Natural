import json
import os
import logging
import shutil
import sys
import threading
from uuid import uuid4, UUID
import signal
import os.path
import webbrowser

from flask import Flask, jsonify, flash, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

from servidor.config import C_RED, C_END
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads')
ALLOWED_EXTENSIONS = {'json'}


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("server")


app = Flask(__name__, static_folder='dist')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
CORS(app, origins="*")


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')



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
        rule = node.get("rule", "{rule}")

        global response
        response.append({
            "uuid" : UUID(uuid),
            "name": name,
            "parentId": parentId,
            "child": [],
            "knowledge_base": knowledge_base,
            "rule": rule
        })

        if child:
            process_tree(child)


@app.route("/api/node", methods=["POST"])
def add_node():
    try:
        local_counter = 1
        local_knowledge_base = {}
        if response:
            return jsonify({"error": "Reset first", "details": str(response)}), 400

        data = request.get_json()
        # logger.debug("POST /api/node - Received data: %s", data)


        if not data.get("expression"):
            logger.warning("POST /api/node - Missing 'expression' parameter in request: %s", data)
            return jsonify({"error": "Missing 'expression' parameter"}), 400

        # Parse the expression
        try:
            parsed_expression = CodeGenerator().generate_code(
                ast_2 := SemanticAnalyzer().analyze(
                    ast_1 := Parser.parse(data.get("expression"), debug=False)
                )
            )

            if not parsed_expression:
                logger.error("POST /api/node - Parsing failed: Missing element in expression")
                return jsonify({"error": "Parsing failed", "details" : str("Missing element")}), 422

        except SyntaxError as e:
            logger.error("POST /api/node - Syntax error: %s", e)
            return jsonify({"error": "Parsing failed", "details": str(e)}), 422

        try:
            for item in data.get("knowledge_base", []):
                # print(item[1])
                key = f"Y{local_counter}"
                local_knowledge_base[key] = item[1]
                local_counter += 1
        except Exception as e:
            logger.error("POST /api/node - Exception: %s", e)
            return jsonify({"error": "Invalid knowledge_base format", "details": str(e)}), 400

        if not response:
            response.append({
                "uuid": uuid4(),
                "name": Parser.parse(parsed_expression),
                "parentId": "",
                "child": [],
                "knowledge_base": local_knowledge_base,
                "rule": "{rule}",
            })

        return jsonify(response), 200

    except Exception as e:
        logger.error("POST /api/node - Exception: %s", e)
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500


@app.route("/api/rules", methods=["POST"])
def apply_rules():
    try:
        data = request.get_json()

        # logger.debug("POST /api/rules - Received data: %s", data)

        parent_id = data.get("id", "0")
        uuid = data.get("uuid", None)

        expression = data.get("expression")
        if not expression:
            logger.warning("POST /api/rules - Missing 'expression' parameter in request: %s", data)
            return jsonify({"error": "Missing 'expression' parameter"}), 400

        try:
            parsed_expression = CodeGenerator().generate_code(
                ast_2 := SemanticAnalyzer().analyze(
                    ast_1 := Parser.parse(expression, debug=False)
                )
            )
        except SyntaxError as e:
            logger.error("POST /api/rules - Syntax error: %s", e)
            return jsonify({"error": "Parsing failed", "details": str(e)}), 422


        knowledge_base_data = data.get("knowledge_base", [])

        if isinstance(knowledge_base_data, list):
            try:
                knowledge_base_data_dict = dict(knowledge_base_data)
            except (ValueError, TypeError) as e:
                logger.error("POST /api/rules - (ValueError, TypeError) error: %s", e)
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

        try:
            if isinstance(knowledge_base_data_dict, dict):
                hypothesis_set = set(knowledge_base_data_dict.items())
            else:
                hypothesis_set = set()
        except Exception as e:
            logger.error("POST /api/rules - Exception: %s", e)
            return jsonify({
                "error": "Failed to process knowledge_base for hypothesis_set",
                "details": str(e)
            }), 400

        auxiliar_formula = data.get("auxiliar_formula", "")

        try:
            rule_name = data.get("rule")
            function_name = 'apply_' + rule_name
            if function_name not in globals():
                logger.warning("POST /api/rules - Rule function '%s' not implemented", function_name)
                return jsonify({"error": f"Rule function '{function_name}' not implemented"}), 400
            function = globals()[function_name]

            result = function(parsed_expression, hypothesis_set, parent_id, auxiliar_formula)

            problem_id = int(parent_id)
            print(C_RED + f"THIS IS THE MAIN PROBLEM ID: {problem_id}\n\n" + C_END)

            global response
            response = filter_recursive_children(parent_id)

            if isinstance(result, list):

                for _, item in enumerate(result, start=2):
                    knowledge_base_item = item.get("knowledge_base", {})

                    if isinstance(knowledge_base_item, list):
                        try:
                            knowledge_base_item = dict(knowledge_base_item)
                        except (ValueError, TypeError) as e:
                            logger.error("POST /api/rules - (ValueError, TypeError) error: %s", e)
                            return jsonify({
                                "error": "Invalid knowledge_base format in item",
                                 "details": f"Expected list of key-value pairs. Error: {str(e)}"
                            }), 400
                    elif not isinstance(knowledge_base_item, dict):
                        return jsonify({
                            "error": "Invalid knowledge_base format in item",
                            "details": "Expected a list of key-value pairs or a dictionary."
                    }), 400

                    new_dict = {
                        **knowledge_base_data_dict,
                        **{
                            key: Parser.parse(val) if isinstance(val, str) else val
                            for key, val in knowledge_base_item.items()
                        }
                    }

                    print(C_RED + f"THIS IS THE NEW PROBLEM PARENT ID {problem_id}\n\n" + C_END)

                    response.append({
                        "uuid" : uuid4(),
                        "name": str(remove_outer_parentheses(Parser.parse(item.get("name")))),
                        "parentId": problem_id,
                        "child": [],
                        "knowledge_base": new_dict,
                        "rule": item.get("rule"),
                    })

            print("Before for_loop entry in response")
            print(f"Just the uuid {uuid}\n\n")

            for entry in response:
                if entry["uuid"] == UUID(uuid):

                    subgoal_rule = None
                    for candidate in response:
                        # print(f"ParentID: {parent_id}")
                        # print(f"CANDIDATE PARENTID. {candidate['parentId']}")
                        if candidate.get("parentId") == parent_id:
                            print(C_RED + f"THIS IS THE CANDIDATE: {candidate}\n\n" + C_END)
                            subgoal_rule = candidate.get("rule")
                            # print(f"SUBGOAL RULE: {subgoal_rule}")
                            if subgoal_rule in ["∧E1","∧E2","∧I","∨E","⟺E1","⟺E2","⟺I","→E","→I","~E","~I","AE","RAA"]:
                                candidate["rule"] = "{rule}"



                    if subgoal_rule is None:
                        return jsonify({
                            "error": "Missing rule term for subgoal",
                            "details": "Could not find matching subgoal rule for substitution"
                        }), 400

                    # print(subgoal_rule)
                    entry["rule"] = "{rule}".format(rule=subgoal_rule)
                    break

            logger.info("POST /api/rules - DONE")
            for i, _ in enumerate(response):
                print(C_RED + f"This is the response: {response[i]}\n\n" + C_END)

        except Exception as e:
            logger.error("POST /api/rules - Exception: %s", e)
            return jsonify({"error": "Function call failed", "details": str(e)}), 500


        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500


@app.route("/api/reset", methods=["POST"])
def reset_data():
    logger.info("Resetting response state.")
    response.clear()
    return jsonify(response), 200


@app.route("/api/save", methods=["POST"])
def save_file():
    data = request.get_json()

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

            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r', encoding='utf-8') as file:
                treedata = file.read()

                print("Debug - treedata:", treedata)
                treedata_json = json.loads(treedata)
                process_tree(treedata_json["tree"])
                print("Processed_tree finished")

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
                        # print(f"Deleted file: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        # print(f"Deleted folder: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        else:
            print(f"Directory not found: {temp_dir}")

    sys.exit(0)


signal.signal(signal.SIGINT, cleanup_and_exit)


def open_browser():
    webbrowser.open_new("http://localhost:3000")


if __name__ == "__main__":

    threading.Timer(1.0, open_browser).start()

    app.run(debug=True, port=3000, use_reloader=False)
