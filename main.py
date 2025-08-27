import os
import requests
import pytz
from datetime import date, timedelta, datetime

def run_bot(request):
    try:
        # Get your sensitive keys from the environment variables
        bot_token = os.environ.get("BOT_TOKEN")
        group_chat_id = os.environ.get("GROUP_CHAT_ID")

        if not bot_token or not group_chat_id:
            print("Error: BOT_TOKEN or GROUP_CHAT_ID environment variable is not set.")
            return "Failure: Environment variables not set.", 500

        # Calculate ballot date (14 days from today)
        def get_ballot_date():
            return date.today() + timedelta(weeks=2)

        # Find epoch for slot selection in url payload
        def get_epoch(hour):
            hourly_seconds = 60 * 60
            two_weeks_seconds = 14 * 24 * hourly_seconds
            # Singapore timezone
            gmt8_timezone = pytz.timezone('Asia/Shanghai')
            start_of_day = datetime.now(gmt8_timezone).replace(hour=0, minute=0, second=0, microsecond=0)
            epoch_timestamp = start_of_day.timestamp()
            # Milliseconds
            return int((epoch_timestamp + two_weeks_seconds + hour * hourly_seconds) * 1000)

        # Strings for different locations
        locations = {
            "senja": "JEBGvnHbjLScZCVrgAorv",
            "<location>": "<string>"
        }

        # Location of interest
        # For loop to generate mulitple links
        location = locations["senja"]

        # Link for the 7pm and 8pm slots (1900hrs and 2000hrs)
        BOOKING_LINK = f"https://activesg.gov.sg/venues/{location}/activities/YLONatwvqJfikKOmB5N9U/timeslots?date={get_ballot_date()}&timeslots={get_epoch(19)}&timeslots={get_epoch(20)}"

        # Create message
        message = (
            f"Ballot for {get_ballot_date()}.\n\n"
            f"🔗 Link: {BOOKING_LINK}"
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