import requests

# API-ключ для News API
API_KEY = "5c3c06bd99e74f35ac4773351c12bffe"
API_URL = "https://newsapi.org/v2/everything"  # URL для News API

# Функция получения новостей по предпочтениям пользователя
def fetch_news(preferences):
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
            filtered_news = process_news(articles)
            return filtered_news
        else:
            print(f"Error: {news_data.get('message')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

# Функция обработки новостей
def process_news(articles):
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
    print(f"Processed {len(filtered_news)} articles.")
    return filtered_news