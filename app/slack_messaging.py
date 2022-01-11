from memory_profiler import profile
import logging

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.config import SLACK_BOT_TOKEN, CHANNEL_ID

client = WebClient(token=SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)


@profile
def send_error_message(app_id, account_id, session_id):
    """
    Send error message to Slack chanel via bot.

    Args:
        app_id (str): application ID.
        account_id (str): account ID.
        session_id (str): session ID.
    """

    if session_id in ['', 'None', None]:
        session_id = 'undefined'

    header_text = (
        f"Event {session_id} "
        "has not been uploaded "
        "because the signatures did not match :ghost: :ghost: :ghost:"
    )
    section_text = (
        f"Session ID:\t{session_id}\n"
        f"Account ID:\t{account_id}\n"
        f"Application ID:\t{app_id}"
    )

    try:
        client.chat_postMessage(
            channel=CHANNEL_ID,
            text="Mr. Badger is watching your API",
            blocks=[
                {"type": "divider"},
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": header_text,
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": section_text,
                    },
                },
            ],
        )

    except SlackApiError as e:
        print(f"Error: {e}")
