FROM python:3.12-slim

WORKDIR /user-service

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8085

CMD [ "python", "app.py" ]