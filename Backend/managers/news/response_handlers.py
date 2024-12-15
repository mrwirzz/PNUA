from flask import jsonify

def handle_response(logger, response, service_name):
    try:
        response_json = response.json()
    except ValueError:
        logger.error(f"invalid JSON response from {service_name}")
        return jsonify({'error': f"Invalid response from {service_name}"}), 500

    if response.status_code == 500:
        logger.error(f"{service_name} endpoint error: {response_json.get('error')}")
        return jsonify({'error': f"{service_name} is unreachable"}), 500
    elif response.status_code == 400:
        logger.error(f"bad request to {service_name} endpoint: {response_json.get('message')}")
        return jsonify({'error': f"Bad request to {service_name} endpoint"}), 400
    elif response.status_code == 200:
        logger.info(f"successfully connected to {service_name}")
        return response_json 
    else:
        logger.error(f"unexpected status code from {service_name}: {response.status_code}")
        return jsonify({'error': f"{service_name} is unreachable"}), 500
