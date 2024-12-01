import requests
import json
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

# API-ключ для News API
API_KEY = "5c3c06bd99e74f35ac4773351c12bffe"
API_URL = "https://newsapi.org/v2/everything"  # URL для News API

# Gmail API: Настройка авторизации
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_credentials():
    """Загрузка учетных данных пользователя."""
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    return creds

# Функция отправки email через Gmail API
def send_email_via_gmail_api(recipient_email, subject, body, user_credentials):
    try:
        # Создаем MIME-объект для email
        message = MIMEText(body)
        message['to'] = recipient_email
        message['subject'] = subject
        
        # Преобразуем сообщение в Base64
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        raw_message = {'raw': raw_message}
        
        # Создаем сервис Gmail API
        service = build('gmail', 'v1', credentials=user_credentials)
        
        # Отправляем сообщение
        result = service.users().messages().send(userId="me", body=raw_message).execute()
        print(f"Email sent to {recipient_email}. Message ID: {result['id']}")
    except Exception as e:
        print(f"An error occurred while sending email: {e}")

# Функция получения новостей по предпочтениям пользователя
def fetch_news(preferences, user_id):
    params = {
        "q": preferences.get("category", "technology"),  # Категория новостей (по умолчанию - технологии)
        "apiKey": API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
    }
    
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        news_data = response.json()
        
        if news_data.get("status") == "ok":
            articles = news_data.get("articles", [])
            filtered_news = process_news(articles, user_id)
            return filtered_news
        else:
            print(f"Error: {news_data.get('message')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

# Функция обработки новостей
def process_news(articles, user_id):
    filtered_news = []
    for article in articles:
        if article["title"] and article["description"]:
            filtered_news.append({
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
                "publishedAt": article["publishedAt"],
                "source": article["source"]["name"]
            })
    print(f"Processed {len(filtered_news)} articles for user {user_id}.")
    send_news_to_user(filtered_news, user_id)
    return filtered_news

# Функция отправки новостей пользователю через Gmail
def send_news_to_user(news, user_id):
    user_email = "user@example.com"  # Здесь укажите email пользователя
    credentials = get_credentials()  # Получите учетные данные Gmail API

    print(f"Sending {len(news)} articles to user {user_id}...")
    
    for article in news:
        title = article["title"]
        description = article["description"]
        url = article["url"]
        body = f"""
        Title: {title}
        Description: {description}
        URL: {url}
        """
        # Отправка через Gmail API
        send_email_via_gmail_api(
            recipient_email=user_email,
            subject=f"Your Daily News: {title}",
            body=body,
            user_credentials=credentials
        )

# Пример вызова
if __name__ == "__main__":
    user_preferences = {"category": "technology"}
    user_id = "user123"
    fetch_news(user_preferences, user_id)