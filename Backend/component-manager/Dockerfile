FROM python:3.9-slim

# Установка рабочей директории
WORKDIR /component_manager
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8085
CMD [ "python", "component_manager.py" ]