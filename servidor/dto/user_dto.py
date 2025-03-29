from flask import Blueprint, jsonify

users_bp = Blueprint("users", __name__)

@users_bp.route("/api/users", methods=["GET"])
def users():
    return jsonify({"users": ["daniel", "pedro", "simao"]})
