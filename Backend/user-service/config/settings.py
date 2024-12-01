class Config:
    DEBUG = True
    TESTING = False
    MONGODB_SETTINGS = {
        "db": "user_service_db",
        "host": "mongodb",  # Имя контейнера
        "port": 27017
    }