from flask import Flask, send_file
import os
import threading
import time
import requests

app = Flask(__name__, static_folder='public')

# Route to serve the index.html file
@app.route('/')
def index():
    return send_file(os.path.join(app.static_folder, "index.html"))

# Function to ping the server periodically
def ping_server():
    sleep_time = 10 * 60  # 10 minutes
    while True:
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
    # Start the ping function in a separate thread
    ping_thread = threading.Thread(target=ping_server, daemon=True)
    ping_thread.start()

    # Start the Flask server
    port = int(os.environ.get("PORT", 3000))  # Default port is 3000
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug=False for production
