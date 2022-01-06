import jwt
import json
import datetime
import os
from fastapi import APIRouter, HTTPException
from starlette import status

from app.forms import Event
from app.send_pubsub_msg import send_message_to_pub_sub_topic
from app.slack_messaging import send_error_message

router = APIRouter()

KEY = os.environ['KEY']

@router.post('/server_event/')
def get_items(*, appId: str, accountId: str, sessionId: str, signature: str, event: Event):
    encoded_signature = jwt.encode(event.dict(), key=KEY, algorithm="HS512")
    if encoded_signature == signature:
        event_plus_timestamp = json.dumps({
            "event_data:": event.dict(), 
            "utc_timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        })
        send_message_to_pub_sub_topic(event_plus_timestamp)
        return {"status": "Event Successfully Sent"}
    else:
        send_error_message(session_id=sessionId, app_id=appId, account_id=accountId)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Signatures didn't Match")
