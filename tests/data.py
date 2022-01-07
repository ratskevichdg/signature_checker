import json
import random

import jwt

from app.config import KEY, PATH_TO_EVENT_DATA_FOR_TEST


# random.seed(42)


def get_test_data():
    json_list = []
    f = open(PATH_TO_EVENT_DATA_FOR_TEST, 'r')
    for i in f.readlines():
        json_file = json.loads(i)
        json_list.append(json_file['event_data'])
    f.close()

    jsons_for_test = random.sample(json_list, 100)

    data_for_request_list = []
    for i in jsons_for_test:
        data_for_request_list.append([
            i, 
            i['appName'],
            i['appUserId'],
            i['sessionId'],
            jwt.encode(i, key=KEY, algorithm="HS512")
        ])

    right_data = data_for_request_list[:int(len(jsons_for_test)/2)]
    wrong_signature_data = data_for_request_list[int(len(jsons_for_test)/2):]

    for i in wrong_signature_data:
        i[4] = i[4].swapcase()

    return (right_data, wrong_signature_data)
