FROM python:3.12-slim

WORKDIR /component_manager

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8085

CMD [ "python", "component_manager.py" ]