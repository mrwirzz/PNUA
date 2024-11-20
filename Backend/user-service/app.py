from flask import Flask
from config.db import init_db
from routes.user_routes import user_routes

app = Flask(__name__)

# Инициализация базы данных
init_db(app)

# Регистрация маршрутов
app.register_blueprint(user_routes, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)