from flask import Flask, request, jsonify
from component_manager.component_manager import DaprComponentManager


app = Flask(__name__)
dapr_manager = DaprComponentManager()

@app.route('/preferences', methods=['POST'])
def subscribe_preferences():
    preferences = request.get_json()
    user_id = preferences.get("user_id")
    category = preferences.get("category", "technology")
    
    # Добавляем предпочтения пользователю через user-service
    user_response = dapr_manager.add_preference_to_user(user_id, category)
    if user_response.get("error"):
        return jsonify({"error": "Failed to update user preferences"}), 500
    
    # Получаем новости через news-service
    news = dapr_manager.fetch_news({"category": category, "user_id": user_id})
    if news.get("error"):
        return jsonify({"error": "Failed to fetch news"}), 500

    # Отправляем email пользователю с новостями
    email_body = "\n".join([f"{article['title']} - {article['url']}" for article in news])
    dapr_manager.send_email_to_user(preferences["email"], "Your Daily News Digest", email_body)
    
    return jsonify({"message": "News sent to user!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)