from flask import Blueprint, request, jsonify
from models.preferences_model import Preference

preferences_blueprint = Blueprint("preferences", __name__)

@preferences_blueprint.route("/", methods=["POST"])
def create_preference():
    """Создание нового предпочтения"""
    try:
        data = request.json
        preference = Preference(**data)
        preference.save()
        return jsonify(preference.to_json()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@preferences_blueprint.route("/", methods=["GET"])
def get_preferences():
    """Получение всех предпочтений"""
    preferences = Preference.objects()
    return jsonify(preferences), 200