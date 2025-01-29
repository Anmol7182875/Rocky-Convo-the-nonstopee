import requests
import time
import sys
import os
import threading

def send_message():
    try:
        # Read the first token from the file
        with open('token.txt', 'r') as file:
            access_token = file.readline().strip()  # Use only the first token

        # Read conversation ID
        with open('convo.txt', 'r') as file:
            convo_id = file.read().strip()

        # Read the file containing messages
        with open('file.txt', 'r') as file:
            text_file_path = file.read().strip()

        with open(text_file_path, 'r') as file:
            messages = file.readlines()

        # Send only the first message
        if messages:
            message = messages[0].strip()  # Only the first message
            url = f"https://graph.facebook.com/v15.0/t_{convo_id}/messages"
            parameters = {
                'access_token': access_token,
                'message': message
            }
            response = requests.post(url, json=parameters)

            if response.ok:
                print(f"[+] Message sent successfully: {message}")
            else:
                print(f"[x] Failed to send message: {response.text}")
        else:
            print("[-] Message file is empty.")

    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == '__main__':
    send_message()
