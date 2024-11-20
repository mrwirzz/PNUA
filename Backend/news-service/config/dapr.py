from dapr.clients import DaprClient

def subscribe_preferences():
    with DaprClient() as client:
        client.subscribe_to_pubsub(
            pubsub_name="messagebus",
            topic_name="preferences-updated",
            callback=process_preferences
        )

def process_preferences(data):
    # Логика обработки предпочтений и получения новостей
    preferences = data.get("preferences")
    user_id = data.get("user_id")
    # Тут будет вызов API новостей с учетом предпочтений
    print(f"Received preferences for user {user_id}: {preferences}")
    # Пример вызова API для новостей
    fetch_news(preferences)
    
def fetch_news(preferences):
    # Пример API-запроса для получения новостей
    import requests
    api_url = "https://newsapi.org/v2/everything"
    params = {
        "q": preferences.get("category", "technology"),
        "apiKey": "your_news_api_key"
    }
    response = requests.get(api_url, params=params)
    news = response.json()
    # Обработка полученных новостей
    process_news(news)

def process_news(news_data):
    # Простой фильтр новостей по ключевым словам или категориям
    filtered_news = [article for article in news_data.get("articles", []) if article["title"]]
    print(f"Processed {len(filtered_news)} articles.")
    # Отправка новостей пользователю (через email, Telegram и т.д.)
    send_news_to_user(filtered_news)

def send_news_to_user(news):
    # Здесь будет логика отправки новостей
    print(f"Sending {len(news)} articles to user.")
    # Например, отправка через Email, Telegram