import os
import requests

def run_bot(request):
    try:
        # Get your sensitive keys from the environment variables
        bot_token = os.environ.get("BOT_TOKEN")
        group_chat_id = os.environ.get("GROUP_CHAT_ID")

        # <-- Insert your logic here -->

        # Create message
        message = (
            f"This is a template for sending a message through a telegram bot."
        )

        api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

        payload = {
            "chat_id": group_chat_id,
            "text": message,
            "parse_mode": "HTML" # Use HTML to avoid escaping
        }
        
        response = requests.post(api_url, data=payload)

        if response.status_code == 200:
            print("Reminder successfully sent!")
            return "Success!"
        else:
            print(f"Failed to send message. Status Code: {response.status_code}, Response: {response.text}")
            return "Failure!", 500
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Failure!", 500       