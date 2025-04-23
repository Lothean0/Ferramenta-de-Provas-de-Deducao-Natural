from flask import Blueprint, jsonify
from servidor.app.utils.response_storage import response

misc_bp = Blueprint("misc", __name__)

@misc_bp.route("/reset", methods=["POST"])
def reset_data():
    print("Reseting data ...")
    response.clear()
    return jsonify(response), 200