from flask import Blueprint, request, jsonify
from models.user_model import User

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/", methods=["POST"])
def create_user():
    """Создание нового пользователя"""
    try:
        data = request.json
        user = User(**data)
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_blueprint.route("/", methods=["GET"])
def get_users():
    """Получение списка всех пользователей"""
    users = User.objects()
    return jsonify(users), 200

@user_blueprint.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    """Получение пользователя по ID"""
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_json()), 200

@user_blueprint.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Удаление пользователя"""
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.delete()
    return jsonify({"message": "User deleted"}), 200