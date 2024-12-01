import requests
import json
from datetime import datetime

# API-ключ для News API
API_KEY = "5c3c06bd99e74f35ac4773351c12bffe"
API_URL = "https://newsapi.org/v2/everything"  # Это URL для API News API

# Функция для получения новостей по предпочтениям пользователя
def fetch_news(preferences, user_id):
    # Строим параметры запроса на основе предпочтений пользователя
    params = {
        "q": preferences.get("category", "technology"),  # Категория новостей (по умолчанию - технологии)
        "apiKey": API_KEY,  # Ваш API-ключ
        "language": "en",  # Язык новостей
        "sortBy": "publishedAt",  # Сортировать по дате публикации
    }
    
    try:
        # Отправляем GET-запрос к News API
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        
        # Обрабатываем полученные данные
        news_data = response.json()
        
        # Если запрос успешный, то получаем и фильтруем новости
        if news_data.get("status") == "ok":
            articles = news_data.get("articles", [])
            filtered_news = process_news(articles, user_id)
            return filtered_news
        else:
            print(f"Error: {news_data.get('message')}")
            return []
    except requests.exceptions.RequestException as e:
        # Обрабатываем исключения при запросах
        print(f"Error fetching news: {e}")
        return []

# Функция для обработки полученных новостей (например, фильтрация по категориям)
def process_news(articles, user_id):
    # Фильтрация новостей (например, по ключевым словам или интересам пользователя)
    filtered_news = []
    
    for article in articles:
        # Пример фильтрации новостей (заголовок и описание должны быть непустыми)
        if article["title"] and article["description"]:
            filtered_news.append({
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
                "publishedAt": article["publishedAt"],
                "source": article["source"]["name"]
            })
    
    print(f"Processed {len(filtered_news)} articles for user {user_id}.")
    
    # После обработки новостей, отправим их пользователю
    send_news_to_user(filtered_news, user_id)
    return filtered_news

# Функция для отправки новостей пользователю (например, по Email или Telegram)
def send_news_to_user(news, user_id):
    # Эта функция будет отправлять новости пользователю через канал связи
    # Пример использования - просто вывод новостей на экран
    print(f"Sending {len(news)} articles to user {user_id}...")
    
    for article in news:
        print(f"\nTitle: {article['title']}")
        print(f"Description: {article['description']}")
        print(f"Published At: {article['publishedAt']}")
        print(f"Source: {article['source']}")
        print(f"URL: {article['url']}")
        
        # Здесь можно добавить код для отправки через Email или Telegram
        # Например, использовать Python Telegram Bot или SMTP для Email.

    # Например, если хотите отправить через Telegram, вам нужно будет подключиться к Telegram Bot API.
    # send_via_telegram(news)  # Для реальной отправки через Telegram

# Пример вызова функции (можно использовать для тестирования)
if __name__ == "__main__":
    # Пример предпочтений пользователя
    user_preferences = {
        "category": "technology"
    }
    
    # Пример ID пользователя
    user_id = "user123"
    
    # Получаем новости и обрабатываем их
    fetch_news(user_preferences, user_id)