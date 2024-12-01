class Config:
    DEBUG = True
    TESTING = False
    MONGODB_SETTINGS = {
        "db": "user_service_db",
        "host": "localhost",
        "port": 27017
    }