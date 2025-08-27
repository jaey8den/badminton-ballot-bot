# Badminton Ballot Bot

This is a script for asking a telegram bot to send daily links for balloting badminton slots on ActiveSG.

I used Google Cloud to deploy as I am simply firing a single API, but any serverless service is fine. The instructions below will be for Google Cloud.

## Steps

This is what I did, there may be better ways to do this.

1. Create a telegram bot from BotFather and add it into your group. Write down the bot token.

2. Type something in your chat. Go to your browser and go to:

   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```

   Find your chat id. It should be a negative number.

3. Download the Google Cloud SDK [here](https://cloud.google.com/sdk/docs/install) and follow its instructions.

4. After initialising gcloud in the terminal, it should prompt you for authentication and asks you to create a project. Create one and name it properly, you will use it later.

5. Go to the directory where you cloned this repo (please only deploy main.py and requirements.txt) and run :

   ```
   gcloud functions deploy run_bot --gen2 --runtime=python311 --region=asia-southeast1 --source=. --entry-point=run_bot --trigger-http --set-env-vars=BOT_TOKEN=<YOUR_BOT_TOKEN>,GROUP_CHAT_ID=<YOUR_CHAT_ID>
   ```

   It should prompt you to enable certain cloud features and retry deployment a few times.

6. To test, go to the url at the last line after deployment. It should say "Success!" if done correctly and "Failure!" if not. If it fails, go to your Google Cloud Console and look at the logs. Debug it yourself.

7. If it is working, go back to your terminal and run:

   ```
   gcloud scheduler jobs create http daily-bot-reminder-job --schedule="0 13 * * *" --uri=<YOUR_BOT_URI> --location="asia-southeast1" --project=<YOUR_PROJECT_NAME>
   ```

   - `--schedule`: how you tell the scheduler when to send the reminder.
     - `0`: 0th minute of the hour
     - `13`: 13 hour
     - `* * *`: every day, every month, and every day of the week
   - `--uri`: a link that will show up near the bottom at the end of a deployment

   Google Cloud follows the UTC, so 13 + 8 = 21, meaning the scheduler is set for 9pm in Singapore.
