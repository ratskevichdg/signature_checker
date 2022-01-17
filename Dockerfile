FROM python:3.9-slim
 
WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app
COPY <path_to_your_google_credentials_json/google_credentials.json> /code/<google_credentials.json>
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV PYTHONPATH=$PWD
ENV PYTHONUNBUFFERED=1
ENV KEY=<your_secret_key>
ENV SLACK_BOT_TOKEN=<your_slack_bot_token>
ENV CHANNEL_ID=<your_slack_channel_id>
ENV GCP_PROJECT_ID=<your_GCP_project_id>
ENV GCP_TOPIC_ID=<your_GCP_PubSub_topic_id>
ENV GOOGLE_APPLICATION_CREDENTIALS=/code/<google_credentials.json>

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]