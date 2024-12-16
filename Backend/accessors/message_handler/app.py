import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from flask import Flask, jsonify, request
import os
import logging

# Flask приложение
app = Flask(__name__)

# Настройка логирования
log_level = os.getenv("LOG_LEVEL", "INFO")
app.logger.setLevel(log_level)
logging.basicConfig(level=log_level)

# Gmail API: Настройка SCOPES
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Функция получения учетных данных Gmail API
def get_credentials():
    """Загрузка учетных данных пользователя для Gmail API."""
    if not os.path.exists('token.json'):
        raise FileNotFoundError("token.json file is missing. Please authenticate the application.")
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    return creds

# Функция создания сообщения для отправки email
def create_email_message(recipient_email, subject, body):
    """Создает MIME сообщение и кодирует его в Base64."""
    message = MIMEText(body)
    message['to'] = recipient_email
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

# Функция отправки email через Gmail API
def send_email_via_gmail_api(recipient_email, subject, body):
    """Отправляет email через Gmail API."""
    try:
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)
        raw_message = create_email_message(recipient_email, subject, body)
        result = service.users().messages().send(userId="me", body=raw_message).execute()
        app.logger.info(f"Email sent to {recipient_email}. Message ID: {result['id']}")
        return True
    except Exception as e:
        app.logger.error(f"An error occurred while sending email: {e}")
        return False

# Эндпоинт для проверки работы сервиса
@app.route('/', methods=['GET'])
def health_check():
    return "<p>Gmail API Email Service is running!</p>", 200

# Эндпоинт для отправки email
@app.route('/send_email', methods=['POST'])
def send_email():
    """Эндпоинт для отправки email."""
    app.logger.info("/send_email endpoint was called")

    email_data = request.get_json()
    if not email_data:
        app.logger.warning("Invalid JSON in request")
        return jsonify({"error": "Invalid JSON"}), 400

    recipient = email_data.get("recipient")
    subject = email_data.get("subject")
    body = email_data.get("body")

    if not recipient or not subject or not body:
        app.logger.warning("Missing fields in JSON request")
        return jsonify({"error": "Missing recipient, subject, or body fields"}), 400

    success = send_email_via_gmail_api(recipient, subject, body)
    if success:
        return jsonify({"message": "Email sent successfully"}), 200
    else:
        return jsonify({"error": "Failed to send email"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8084)
