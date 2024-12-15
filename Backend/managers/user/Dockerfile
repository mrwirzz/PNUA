FROM python:3.12-slim

WORKDIR /user

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "python", "app.py" ]