from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Определение необходимых разрешений для Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authorize_gmail():
    # Инициализация потока авторизации с использованием файла client_secrets
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    credentials = flow.run_local_server(port=0)  # Открытие веб-сервера для получения авторизационного кода
    with open('token.json', 'w') as token_file:
        token_file.write(credentials.to_json())  # Сохранение токена в файл
    print("Authorization complete.")

authorize_gmail()