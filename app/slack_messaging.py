from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from loguru import logger

from app.config import SLACK_BOT_TOKEN, CHANNEL_ID

client = WebClient(token=SLACK_BOT_TOKEN)


def send_error_message(app_id_deque, account_id_deque, session_id_deque):
    """
    Send error messages in batch of 20 to Slack chanel via bot.
    Args:
        app_id_deque (deque): deque of application IDs.
        account_id_deque (deque): deque of account IDs.
        session_id_deque (deque): deque of session IDs.
    """

    header_text = (
        "Events "
        "have not been uploaded "
        "because the signatures did not match :ghost: :ghost: :ghost:"
    )
    section_text = (
        f":poop: Events ID:\t{', '.join(session_id_deque)}\n"
        f":poop: Accounts ID:\t{', '.join(account_id_deque)}\n"
        f":poop: Application ID:\t{', '.join(app_id_deque)}"
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
        logger.error(f"Slack Error: {e}")
