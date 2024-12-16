from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/preferences', methods=['POST'])
def add_preferences():
    data = request.get_json()
    user_id = data["user_id"]
    preference = data["preference"]
    
    
    response = add_preference_to_user(user_id, preference)
    if "error" in response:
        return jsonify({"error": "Failed to update user preferences"}), 500
    
    return jsonify({"message": "Preferences updated successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)