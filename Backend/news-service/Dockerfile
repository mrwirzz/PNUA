FROM python:3.12-slim

WORKDIR /news-service

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8085

CMD [ "python", "app.py" ]