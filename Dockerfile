FROM python:3.9
 
WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
COPY ./app /code/app

COPY <path_to_your_gcp_credentials_json_file>/<your_gcp_credentials_json_file>.json /code/<your_gcp_credentials_json_file>.json

ENV GOOGLE_APPLICATION_CREDENTIALS=="/code/<your_gcp_credentials_json_file>.json"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
