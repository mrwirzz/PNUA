from dapr.clients import DaprClient
import json

def connect_to_ai_summarizer(raw_preferences):
    request_string = json.dumps({"raw_preferences": raw_preferences})

    with DaprClient() as d:
        resp = d.invoke_method('ai_summarizer', 'summarize_preferences', data=request_string, http_verb='post')
    return resp

def connect_to_news_collector(preferences):
    request_string = json.dumps({"body": preferences})

    with DaprClient() as d:
        resp = d.invoke_method('news_collector', 'get_news', data=request_string, http_verb='post')
    return resp

def connect_to_message_handler(recipient, subject, body):
    request_string = json.dumps({"recipient": recipient, "subject": subject, "body": body})

    with DaprClient() as d:
        resp = d.invoke_method('message_handler', 'send_message', data=request_string, http_verb='post')
    return resp

def user_manager_callback(message, user_id):
    response_string = json.dumps({"message": message, "user_id": user_id})

    with DaprClient() as d:
        resp = d.invoke_method("user_manager", "callback", data=response_string, http_verb='post')
    return resp
