from flask import Flask
from routes.user_routes import user_blueprint
from routes.preferences_routes import preferences_blueprint
from config.settings import Config

app = Flask(__name__)
app.config.from_object(Config)

# Регистрация маршрутов
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(preferences_blueprint, url_prefix="/preferences")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)