from flask import Flask, send_file, jsonify, request
import os
import threading
import time
import requests

app = Flask(__name__, static_folder='public')

# Global offline mode flag
OFFLINE_MODE = True  # Change to False to enable live server pinging

# Route to serve the index.html file
@app.route('/')
def index():
    return send_file(os.path.join(app.static_folder, "index.html"))

# Route to simulate or actually handle API requests
@app.route('/api/send-message', methods=['POST'])
def send_message():
    try:
        data = request.json  # Get JSON data from the POST request
        message = data.get('message', '')
        if not message:
            return jsonify({"status": "error", "message": "Message content is missing!"})

        # Offline mode simulation
        if OFFLINE_MODE:
            return jsonify({"status": "success", "message": f"[OFFLINE MODE] Simulated message: {message}"})

        # Actual request logic for live mode
        url = 'https://your_actual_server_url.com'
        response = requests.post(url, json=data, timeout=10)

        if response.ok:
            return jsonify({"status": "success", "message": "Message sent successfully!"})
        else:
            return jsonify({"status": "error", "message": f"Failed to send message. Error: {response.text}"})

    except requests.RequestException as e:
        return jsonify({"status": "error", "message": f"Request failed: {e}"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Unexpected error: {e}"})

# Function to ping the server periodically
def ping_server():
    sleep_time = 10 * 60  # 10 minutes
    while not OFFLINE_MODE:  # Only ping in live mode
        time.sleep(sleep_time)
        try:
            response = requests.get('https://your_actual_server_url.com', timeout=10)
            print(f"Pinged server with response: {response.status_code}")
        except requests.Timeout:
            print("Couldn't connect to the site: Timeout!")
        except requests.RequestException as e:
            print(f"Ping error: {e}")

# Start the Flask server and the ping thread
if __name__ == "__main__":
    # Start the ping function in a separate thread if not in offline mode
    if not OFFLINE_MODE:
        ping_thread = threading.Thread(target=ping_server, daemon=True)
        ping_thread.start()

    # Start the Flask server
    port = int(os.environ.get("PORT", 3000))  # Default port is 3000
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug=False for production
