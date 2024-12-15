FROM python:3.12-slim

WORKDIR /ai

COPY . .

RUN pip install -r requirements.txt


EXPOSE 8084

CMD [ "python", "app.py" ]