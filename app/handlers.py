import jwt
import json
import datetime
from memory_profiler import profile
from fastapi import APIRouter, HTTPException, Request, Response
from starlette import status
from typing import Optional

from app.send_pubsub_msg import send_message_to_pub_sub_topic
from app.slack_messaging import send_error_message
from app.utilities import find_query_parameter
from app.config import KEY
from logger import logger

router = APIRouter()


@profile
@logger.catch
@router.post("/server_event/")
async def get_items(
        *,
        appId: Optional[str] = None,
        accountId: Optional[str] = None,
        sessionId: Optional[str] = None,
        signature: Optional[str] = None,
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
    try:
        request_body = await event.json()
        appId = find_query_parameter(appId, request_body, 'appName')
        accountId = find_query_parameter(accountId, request_body, 'appUserId')
        sessionId = find_query_parameter(sessionId, request_body, 'sessionId')

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
            # send error message to Slack chanel via bot
            send_error_message(
                session_id=sessionId,
                app_id=appId,
                account_id=accountId
            )
            return Response("Signatures didn't Match", status_code=status.HTTP_403_FORBIDDEN)
    except HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        logger.error("Internal server error")
        return Response("Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
