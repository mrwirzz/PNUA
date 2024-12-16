from flask import Flask, g, jsonify, request
from google.protobuf.json_format import MessageToDict
from prompt_model import model
import os

# Инициализация приложения Flask
app = Flask(__name__)

# Настройка уровня логирования
log_level = os.getenv("LOG_LEVEL", "INFO")
app.logger.setLevel(log_level)

@app.route('/', methods=['GET'])
def hello_world():
    """Простой эндпоинт для проверки работы приложения."""
    return "<p>Hello from app!</p>"

@app.route('/summarize_preferences', methods=['POST'])
def summarize():
    """Эндпоинт для обработки предпочтений пользователя."""
    app.logger.info('/summarize_preferences endpoint called')

    # Получаем данные из запроса
    raw_preferences_data = request.get_json()
    
    if not raw_preferences_data:
        return jsonify({'message': 'Invalid JSON'}), 400

    raw_preferences_body = raw_preferences_data.get("raw_preferences", "").strip()

    if not raw_preferences_body:
        return jsonify({'no_topic': True, 'preferences': 'empty preferences'}), 200

    try:
        # Инициализация чат-сессии с AI
        chat_session = model.start_chat(history=[])
        ai_response = chat_session.send_message(raw_preferences_body)
        app.logger.info('Received response from AI')

        # Преобразование ответа в словарь
        ai_response_dict = MessageToDict(ai_response._result._pb)
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': 'Internal chat session error'}), 500

    # Извлечение предпочтений из ответа AI
    preferences = (
        ai_response_dict.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text")
        .strip()
    )

    # Обработка различных случаев
    if preferences == 'no topic':
        return jsonify({'no_topic': True, 'preferences': preferences}), 200
    elif preferences is None:
        app.logger.warning(f"Unsuccessful parsing of AI response: {ai_response_dict}")
        return jsonify({'error': 'Unsuccessful JSON parsing'}), 500

    app.logger.info(f"Parsed response from AI: {preferences}")
    return jsonify({'no_topic': False, 'preferences': preferences}), 200

if __name__ == "__main__":
    # Запуск приложения Flask
    app.run(host="0.0.0.0", port=8082)
