FROM python:3.12-slim

WORKDIR /news

COPY . .

RUN pip install -r requirements.txt


EXPOSE 8081

CMD [ "python3", "app.py" ]