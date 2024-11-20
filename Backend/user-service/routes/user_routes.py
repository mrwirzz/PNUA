from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from config.db import mongo

import uuid
import json

user_routes = Blueprint("user_routes", __name__)
user_model = UserModel(mongo.db)

@user_routes.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400
    user_id = str(uuid.uuid4())  # Генерация уникального идентификатора
    data["_id"] = user_id
    user_model.create_user(data)
    return jsonify({"message": "User created successfully", "id": user_id}), 201

@user_routes.route("/users", methods=["GET"])
def get_users():
    users = user_model.get_users()
    return jsonify(users), 200

@user_routes.route("/users/<user_id>/preferences", methods=["PUT"])
def update_preferences(user_id):
    preferences = request.json.get("preferences", {})
    result = user_model.update_preferences(user_id, preferences)
    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404

    # Публикация обновлений через Dapr
    from dapr.clients import DaprClient
    with DaprClient() as client:
        client.publish_event(
            pubsub_name="messagebus",
            topic_name="preferences-updated",
            data=json.dumps({"user_id": user_id, "preferences": preferences}),
            data_content_type="application/json",
        )

    return jsonify({"message": "Preferences updated successfully"}), 200

@user_routes.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = user_model.delete_user(user_id)
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 200