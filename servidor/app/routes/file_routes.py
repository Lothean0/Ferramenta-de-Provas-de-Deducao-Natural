import os
import json
from flask import Blueprint, request, jsonify, flash, current_app
from werkzeug.utils import secure_filename
from servidor.app.utils.response_storage import response, increment_counter

file_bp = Blueprint("file", __name__)

def allowed_file(filename):
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@file_bp.route("/file", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        with open(file_path, 'r') as f:
            treedata = f.read()

        return jsonify({"filename": treedata}), 200

    return jsonify({"error": "File not allowed"}), 400

@file_bp.route("/save", methods=["POST"])
def save_file():
    data = request.get_json()
    download_folder = current_app.config['DOWNLOAD_FOLDER']

    counter = increment_counter()
    filename = f'tree-data-{counter}.json'

    if not allowed_file(filename):
        return jsonify({"error": "Invalid file type"}), 400

    tree_data_str = json.dumps(data, indent=2)

    try:
        with open(os.path.join(download_folder, filename), 'w') as f:
            f.write(tree_data_str)

        return jsonify({
            "message": "Data saved to file successfully!",
            "number": counter
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
