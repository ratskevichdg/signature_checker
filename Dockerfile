FROM python:3.9
 
WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
COPY ./app /code/app

COPY <path_to_your_gcp_credentials_json_file>/<your_gcp_credentials_json_file>.json /code/<your_gcp_credentials_json_file>.json 

ENV KEY="<your_secret_key_for_encrypting>"
ENV SLACK_BOT_TOKEN="<your_slack_bot_token>"
ENV CHANNEL_ID="<your_slack_channel_id>"
ENV GCP_PROJECT_ID="<your_gcp_project_id>"
ENV GCP_TOPIC_ID="<your_gcp_pub_sub_topic_id>"
ENV GOOGLE_APPLICATION_CREDENTIALS="/code/<your_gcp_credentials_json_file>.json"
ENV PATH_TO_EVENT_DATA_FOR_TEST="<path_to_file_with_event_data_for_testing>"
 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]


