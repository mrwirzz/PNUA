from flask import Flask, g, jsonify, request
import os
import connectors as my_dapr
from response_handlers import handle_response
from datetime import datetime

app = Flask(__name__)

log_level = os.getenv("LOG_LEVEL", "INFO")
app.logger.setLevel(log_level)

@app.route('/', methods=['GET'])
def hello_world():
    return "<p>Hello from app!</p>"

@app.route('/news_request_queue', methods=['POST'])
def request_queue():
    app.logger.info('/news_request_queue endpoint got called')

    user_data = request.get_json()
    user_id = user_data.get("user_id")
    raw_preferences = user_data.get("raw_preferences")
    user_email = user_data.get("email")
    if raw_preferences is None or user_email is None:
        app.logger.warning('endpoint got invalid request JSON')
        my_dapr.user_manager_callback('Please, enter your email and preferenses', user_id)
        return jsonify({'message': 'Invalid JSON'}), 200 #400
    
    ai_summarizer_response = my_dapr.connect_to_ai_summarizer(raw_preferences)
    result = handle_response(app.logger, ai_summarizer_response, 'AI summarizer')
    if isinstance(result, tuple): return result # Check if it's an error response
    ai_summarizer_response = result
 
    if ai_summarizer_response['no_topic'] == True:
        app.logger.warning(f"Ai couldn't get the topic right:{ai_summarizer_response['preferences']}")
        my_dapr.user_manager_callback('Try enter another preferenses.', user_id)
        return jsonify({'error': "Preferenses not found"}), 200 #422
    
    news_collector_response = my_dapr.connect_to_news_collector(ai_summarizer_response['preferences'])
    result = handle_response(app.logger, news_collector_response, 'news collector')
    if isinstance(result, tuple): return result # Check if it's an error response
    news_collector_response = result

    if news_collector_response['empty_page'] == True:
        app.logger.warning(f"No relevant news by this theme: {ai_summarizer_response['preferences']}")
        my_dapr.user_manager_callback('Relevant news not found.', user_id)
        return jsonify({'error': 'Relevant news not found'}), 200 #422
     
    subject = "Your personal news digest"
    email_body = ""
    for news in news_collector_response['lateat_news']:
        title = f"<a href='{news['url']}' style='font-weight:bold; text-decoration:none; color:blue;'>{news['title']}</a>"
        publication_date = datetime.strptime(news['publication_date'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M")
        email_body += f"<p>{title}<br>{publication_date}</p>"
    
    # app.logger.warning(f"Ai couldn't get the topic right:{ai_summarizer_response['preferences']}")
    message_handler_response = my_dapr.connect_to_message_handler(user_email, subject, email_body)
    result = handle_response(app.logger, message_handler_response, 'message handler')
    if isinstance(result, tuple): return result # Check if it's an error response

    my_dapr.user_manager_callback('Message sent! Check your Email.', user_id)
    return jsonify({'message': 'Email sent!'}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
