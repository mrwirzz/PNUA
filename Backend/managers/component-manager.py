import dapr.clients
from dapr.clients.grpc._state import StateClient
import json

class DaprComponentManager:
    def __init__(self, dapr_client=None):
        self.client = dapr_client or dapr.clients.DaprClient()

    def user_manager_callback(self, message, user_id):
        """Callback для пользователя"""
        data = json.dumps({"message": message, "user_id": user_id}).encode("utf-8")
        self.client.publish_event(
            pubsub_name="user-manager-pubsub",  # Предположим, что у нас есть такой pubsub
            topic="user-callback",
            data=data
        )

    def add_preference_to_user(self, user_id, preference):
        """Добавить предпочтение пользователю через user-service"""
        response = self.client.invoke_method(
            app_id="user-service",
            method_name="add_preference_to_user",
            data=json.dumps({"user_id": user_id, "preference": preference}).encode("utf-8")
        )
        return response.json()

    def fetch_news(self, preferences):
        """Запрос новостей через news-service"""
        response = self.client.invoke_method(
            app_id="news-service",
            method_name="fetch_news",
            data=json.dumps(preferences).encode("utf-8")
        )
        return response.json()

    def send_email_to_user(self, email, subject, body):
        """Отправка email через news-service (Gmail API)"""
        response = self.client.invoke_method(
            app_id="news-service",
            method_name="send_news_to_user",
            data=json.dumps({"email": email, "subject": subject, "body": body}).encode("utf-8")
        )
        return response.json()