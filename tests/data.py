import json
import random

import jwt

from app.config import KEY, PATH_TO_EVENT_DATA_FOR_TEST


# uncomment this to set random seed
# random.seed(42)


def get_test_data():
    """
    Function for creating and spliting dataset for unit testing.

    Returns:
        tuple: 0 element - list with valid signatures.
               1 element - list with invalid signatures.
    """

    # read file with events and add every event to json_list
    with open(PATH_TO_EVENT_DATA_FOR_TEST, "r") as file:
        json_list = [
            json.loads(line)["event_data"] for line in file.readlines()
        ]

    # randomly sample 100 events
    jsons_for_test = random.sample(json_list, 100)

    # extract event_data, app_id, account_id, session_id and signature
    # in one list for every event
    # and add this event list to common list
    data_for_request_list = [
        [
            single_event,
            single_event["appName"],
            single_event["appUserId"],
            single_event["sessionId"],
            jwt.encode(single_event, key=KEY, algorithm="HS512"),
        ]
        for single_event in jsons_for_test
    ]

    # split the list of events into two lists
    right_signature_data = data_for_request_list[:int(len(jsons_for_test) / 2)]
    wrong_signature_data = data_for_request_list[int(len(jsons_for_test) / 2):]

    # messing up the signatures in the list
    for i in wrong_signature_data:
        i[4] = i[4].swapcase()

    return (right_signature_data, wrong_signature_data)
