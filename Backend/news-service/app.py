from flask import Flask
from config.dapr import subscribe_preferences

app = Flask(__name__)

# Используем контекст приложения для инициализации подписки
with app.app_context():
    try:
        # Инициализация подписки на Pub/Sub
        subscribe_preferences()
        print("Dapr subscription initialized successfully.")
    except Exception as e:
        print(f"Error initializing Dapr subscription: {e}")

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)