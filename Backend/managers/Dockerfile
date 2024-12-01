FROM python:3.9-slim

# Установка зависимостей для Dapr и необходимых инструментов
RUN apt-get update && apt-get install -y curl bash && \
    curl -fsSL https://github.com/dapr/dapr/releases/download/v1.13.6/daprd_linux_amd64.tar.gz -o /tmp/daprd_linux_amd64.tar.gz && \
    mkdir -p /root/.dapr/bin && \
    tar -xvzf /tmp/daprd_linux_amd64.tar.gz -C /root/.dapr/bin && \
    echo "Dapr installed" && \
    ls -la /root/.dapr/bin  # Проверка содержимого каталога

# Добавление Dapr в PATH
ENV PATH="/root/.dapr/bin:$PATH"

# Проверим, что Dapr находится в PATH
RUN echo "Dapr path: $PATH"

# Проверим, что Dapr был установлен
RUN ls /root/.dapr/bin  # Проверим, что файлы действительно распакованы

# Использование официального скрипта установки Dapr с bash
RUN curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash

# Установка рабочей директории
WORKDIR /app

# Копирование файлов с зависимостями
COPY requirements.txt requirements.txt

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Убедимся, что Dapr установлен и доступен
RUN dapr --version

# Команда для запуска компонента-менеджера
CMD ["dapr", "run", "--app-id", "component-manager", "--app-port", "5000", "--", "python", "component_manager.py"]
