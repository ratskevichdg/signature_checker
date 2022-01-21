from collections import deque

import jwt
import json
import datetime
from fastapi import APIRouter, HTTPException, Request, Response, Query
from starlette import status
from typing import Optional
from loguru import logger

from app.send_pubsub_msg import send_message_to_pub_sub_topic
from app.slack_messaging import send_error_message
from app.config import KEY

router = APIRouter()

bad_signature_app_id_deque = deque()
bad_signature_account_id_deque = deque()
bad_signature_session_id_deque = deque()


@logger.catch
@router.post("/server_event/")
async def get_items(
        *,
        app_id: Optional[str] = Query(None, alias="appId"),
        account_id: Optional[str] = Query(None, alias="accountId"),
        session_id: Optional[str] = Query(None, alias="sessionId"),
        signature: Optional[str] = Query(None, alias="signature"),
        event: Request
):
    """
    Processes the received request with the event.
    Args:
        app_id (str): application ID.
        account_id (str): account ID.
        signature (str): signature.
        event (Request): request body.
        session_id (Optional[str]): signature. Defaults to 'undefined'.
    Raises:
        HTTPException: raises 403 exception
                       when signatures do not match.
    Returns:
        dict: status message.
    """
    # get the request body
    try:
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
            return Response("Event Successfully Sent", status_code=status.HTTP_200_OK)
        else:
            bad_signature_app_id_deque.append('undefined' if app_id in ['', None] else app_id)
            bad_signature_account_id_deque.append('undefined' if account_id in ['', None] else account_id)
            bad_signature_session_id_deque.append('undefined' if session_id in ['', None] else session_id)
            if len(bad_signature_session_id_deque) == 20:
                # send error message to Slack chanel via bot
                send_error_message(
                    app_id_deque=bad_signature_app_id_deque,
                    account_id_deque=bad_signature_account_id_deque,
                    session_id_deque=bad_signature_session_id_deque
                )
                bad_signature_app_id_deque.clear()
                bad_signature_account_id_deque.clear()
                bad_signature_session_id_deque.clear()
            return Response("Signatures didn't Match", status_code=status.HTTP_403_FORBIDDEN)
    except HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        logger.error("Internal server error")
        return Response("Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
