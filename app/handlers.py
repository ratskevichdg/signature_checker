import jwt
import json
import datetime
from fastapi import APIRouter, HTTPException, Request
from starlette import status
from typing import Optional

from app.send_pubsub_msg import send_message_to_pub_sub_topic
from app.slack_messaging import send_error_message
from app.config import KEY


router = APIRouter()


@router.post("/server_event/")
async def get_items(
    *,
    appId: str,
    accountId: str,
    sessionId: Optional[str] = "undefined",
    signature: str,
    event: Request
):
    """
    Processes the received request with the event.

    Args:
        appId (str): application ID.
        accountId (str): account ID.
        signature (str): signature.
        event (Request): request body.
        sessionId (Optional[str]): signature. Defaults to 'undefined'.

    Raises:
        HTTPException: raises 403 exception
                       when signatures does not match.

    Returns:
        dict: status message.
    """
    # get the request body
    request_body = await event.json()
    # encode request body to get signature
    encoded_signature = jwt.encode(
        request_body,
        key=KEY,
        algorithm="HS512"
    )
    if encoded_signature == signature:
        # add current timestamp to request body
        event_plus_timestamp = json.dumps(
            {
                "event_data:": request_body,
                "utc_timestamp": datetime.datetime.utcnow().strftime(
                    "%Y-%m-%dT%H:%M:%S"
                ),
            }
        )
        # send message to Google Pub/Sub topic
        send_message_to_pub_sub_topic(event_plus_timestamp)
        return {"status": "Event Successfully Sent"}
    else:
        # send error message to Slack chanel via bot
        send_error_message(
            session_id=sessionId,
            app_id=appId,
            account_id=accountId
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Signatures didn't Match"
        )
