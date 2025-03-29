from flask import Blueprint, request, jsonify

logic_bp = Blueprint("logic", __name__)

@logic_bp.route("/api/checkExpression", methods=["POST"])
def check_expression():
    data = request.json
    print("Received:", data)
    return jsonify({"message": "Data received successfully", "received": data}), 400
