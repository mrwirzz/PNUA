FROM python:3.12-slim

WORKDIR /collector

COPY . .

RUN pip install -r requirements.txt


EXPOSE 8083

CMD [ "python", "app.py" ]