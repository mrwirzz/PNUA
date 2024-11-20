from flask import Flask
from config.dapr import subscribe_preferences

app = Flask(__name__)

@app.before_first_request
def init_dapr_subscription():
    # Инициализация подписки на Pub/Sub
    subscribe_preferences()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)