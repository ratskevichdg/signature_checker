import logging

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.config import SLACK_BOT_TOKEN, CHANNEL_ID


client = WebClient(token=SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)

def send_error_message(app_id, account_id, session_id):
    try:
        result = client.chat_postMessage(
            channel=CHANNEL_ID,
            text='Mr. Badger is watching your API',
            blocks=[
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Event {session_id} has not been downloaded because the signatures did not match :ghost: :ghost: :ghost:"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Session ID:\t{session_id}\nAccount ID:\t{account_id}\nApplication ID:\t{app_id}"
                    }
                }
            ]
        )

    except SlackApiError as e:
        print(f"Error: {e}")
