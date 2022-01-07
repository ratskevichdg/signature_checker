import os

from starlette.config import Config

dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = dir_path[:-3]
config = Config(f'{root_dir}.env')

KEY = config('KEY', cast=str)
SLACK_BOT_TOKEN = config('SLACK_BOT_TOKEN', cast=str)
CHANNEL_ID = config('CHANNEL_ID', cast=str)
GCP_PROJECT_ID = config('GCP_PROJECT_ID', cast=str)
GCP_TOPIC_ID = config('GCP_TOPIC_ID', cast=str)
GOOGLE_APPLICATION_CREDENTIALS = config('GOOGLE_APPLICATION_CREDENTIALS', cast=str)
PATH_TO_EVENT_DATA_FOR_TEST = config('PATH_TO_EVENT_DATA_FOR_TEST', cast=str)