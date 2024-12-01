from dapr.clients import DaprClient
import requests

def subscribe_preferences():
    with DaprClient() as client:
        client.subscribe_to_pubsub(
            pubsub_name="messagebus",
            topic_name="preferences-updated",
            callback=process_preferences
        )

def process_preferences(data):
    preferences = data.get("preferences")
    user_id = data.get("user_id")
    
    if not preferences or not user_id:
        print("Error: Missing preferences or user_id.")
        return
    
    print(f"Received preferences for user {user_id}: {preferences}")
    fetch_news(preferences)

def fetch_news(preferences):
    api_url = "https://newsapi.org/v2/everything"
    params = {
        "q": preferences.get("category", "technology"),
        "apiKey": "your_news_api_key"
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        news = response.json()
        process_news(news)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")

def process_news(news_data):
    filtered_news = [article for article in news_data.get("articles", []) if article["title"]]
    print(f"Processed {len(filtered_news)} articles.")
    send_news_to_user(filtered_news)

def send_news_to_user(news):
    print(f"Sending {len(news)} articles to user.")
    try:
        # Логика отправки через Email или Telegram
        pass
    except Exception as e:
        print(f"Error sending news: {e}")