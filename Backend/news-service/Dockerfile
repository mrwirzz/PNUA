FROM python:3.9-slim

# Установка зависимостей для Dapr
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://github.com/dapr/dapr/releases/download/v1.13.6/daprd_linux_amd64.tar.gz -o /tmp/daprd_linux_amd64.tar.gz && \
    mkdir -p /root/.dapr/bin && \
    tar -xvzf /tmp/daprd_linux_amd64.tar.gz -C /root/.dapr/bin && \
    echo "Dapr installed, listing /root/.dapr/bin/..." && \
    ls /root/.dapr/bin/
# Проверка, что Dapr установлен
RUN echo "Dapr installed, listing /root/.dapr/bin/..." && \
    ls /root/.dapr/bin/

# Установка переменной окружения PATH для доступа к daprd
ENV PATH="/root/.dapr/bin:$PATH"

# Установка рабочей директории
WORKDIR /app

# Установка зависимостей Python
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов компонента Dapr
COPY ./components /root/.dapr/components

# Установка прав на выполнение для daprd
RUN chmod +x /root/.dapr/bin/daprd

# Копирование исходного кода
COPY . .

# Команда для запуска приложения и Dapr Sidecar
CMD ["dapr", "run", "--app-id", "news-service", "--app-port", "5002", "--components-path", "/app/components", "--", "python", "app.py"]