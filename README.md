# Signature Checker

#### The program is an API for checking request signatures. If signature is correct, the timestamp will added to the Event from the request and sent to Google Pub/Sub. Otherwise, the API sends an error message to the specified Slack channel.

## :hammer: Installation :hammer:

First fork the repo then do a git clone.

```
git clone https://github.com/<yournamehere>/signature_checker.git
```

You should also have *Docker*, *Slack* workspace with *Bot* connected, and *Google Cloud Platform Project* with *Pub/Sub
Topic* connected. Open a `Dockerfile` and add your environmental variables:

```
FROM python:3.9
 
WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app
COPY <path_to_your_google_credentials_json/google_credentials.json> /code/<google_credentials.json>
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV KEY=<your_secret_key>
ENV SLACK_BOT_TOKEN=<your_slack_bot_token>
ENV CHANNEL_ID=<your_slack_channel_id>
ENV GCP_PROJECT_ID=<your_GCP_project_id>
ENV GCP_TOPIC_ID=<your_GCP_PubSub_topic_id>
ENV GOOGLE_APPLICATION_CREDENTIALS="/code/<google_credentials.json>

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

### Build the Docker Image

Now that all the files are in place, let's build the container image.

- Go to the project directory (in where your  `Dockerfile`  is, containing your  `app`  directory).
- Build your FastAPI image:

```
docker build -t sign_checker_image .
```

### Start the Docker Container

- Run a container based on your image:

```
docker run -d --name sign_checker -p 80:80 sign_checker_image
```

## :muscle: Testing :muscle:

For test you can use the CURL queries provided below to test These are queries where the signatures match

```
curl -X 'POST' \
  'http://127.0.0.1/server_event/?appId=casino&accountId=80931046&sessionId=6830887843&signature=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjp7ImV2ZW50RGF0YSI6eyJldmVudFR5cGUiOiJlYWdsdmlldyIsImZpcnN0X3RpbWVfbG9naW4iOjAsInRpbWVfc2luY2Vfc3RhcnQiOjEsInZhbHVlIjoxLCJwbGF0Zm9ybUFjY291bnRJZCI6MjEyOTY2NDUwfSwiZGV2aWNlSW5mbyI6eyJ0aGlyZFBhcnR5VHJhY2tpbmdFbmFibGVkIjoxLCJpZmEiOiI1QjE2RTREMS0xRjY4LTQyNzQtQTNGQi1DRkJDOUZCOTYyM0EiLCJhcHBUcmFja2luZ1RyYW5zcGFyZW5jeVN0YXR1cyI6IjMiLCJpZmFFbmFibGVkIjowfSwiZXZlbnROYW1lIjoiZWFnbHZpZXciLCJkZXZpY2VNb2RlbCI6ImlQYWQiLCJvc1ZlcnNpb24iOiIxNS4xIiwic2NyZWVuUmVzb2x1dGlvbiI6IjgzNHgxMTEyIiwiYnVuZGxlSWQiOiJjb20uYmlnZmlzaGdhbWVzLmJmY2FzaW5vdW5pdmVyc2FsZnJlZW1pdW0iLCJhcHBTdG9yZSI6IiIsImFwcFN0b3JlSWQiOiIiLCJkZXZpY2VCcmFuZCI6IiIsImRldmljZUNhcnJpZXIiOiIiLCJkZXZpY2VJZGlvbSI6IiIsInByb2Nlc3NvclR5cGUiOiIiLCJvc0luZm8iOiIiLCJnZW9JcCI6IiJ9LCJhcHBVc2VySWQiOiI4MDkzMTA0NiIsImV2ZW50VHlwZSI6ImN1c3RvbSIsInNlc3Npb25JZCI6NjgzMDg4Nzg0MywicGxheVNlc3Npb25JZCI6NjgzMDg4Nzg0MywicGxhdGZvcm0iOiJpb3MiLCJhcHBWZXJzaW9uIjoiMTMuMy4yIiwiaXAiOiI3Mi4xODUuNzEuMTQiLCJsYW5ndWFnZUNvZGUiOiJlbl9VUyIsImNsaWVudFRpbWV6b25lT2Zmc2V0IjotMTgwMDAwMDAsInJhdmVJZCI6ImUxNjQ2M2JhZWViNTQ4YmI4MWFmYjY5NmU4M2NlOWZkIiwiZW52aXJvbm1lbnQiOiJwcm9kIiwiYXBwTmFtZSI6ImNhc2lubyIsInRpbWVzdGFtcENsaWVudCI6MTYzOTE4NDM5OSwiY2xpZW50RXZlbnRJZCI6IjM5NzU4NTNjLWQ2MjktNGEzYi04YzBiLTFkZjI0MGEyNGYzMiIsImJmZ1Nka1ZlcnNpb24iOiIwNjA5MDAwMCIsImJmZ3VkaWQiOiIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIiwidGltZXN0YW1wU2VydmVyIjoiIiwiYXBwQnVpbGRWZXJzaW9uIjoiIiwibXNnUGF5bG9hZFZlcnNpb24iOiIiLCJjb3VudHJ5Q29kZSI6IiJ9.7vaHHDXNEA479lzppOr7OTWHiLLPegiBx0ONAF0tfB0F-BvAPzFoBFdesResULlmPLRDWR-_fLE_GJraa1Hq3Q' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"data":{"eventData":{"eventType":"eaglview","first_time_login":0,"time_since_start":1,"value":1,"platformAccountId":212966450},"deviceInfo":{"thirdPartyTrackingEnabled":1,"ifa":"5B16E4D1-1F68-4274-A3FB-CFBC9FB9623A","appTrackingTransparencyStatus":"3","ifaEnabled":0},"eventName":"eaglview","deviceModel":"iPad","osVersion":"15.1","screenResolution":"834x1112","bundleId":"com.bigfishgames.bfcasinouniversalfreemium","appStore":"","appStoreId":"","deviceBrand":"","deviceCarrier":"","deviceIdiom":"","processorType":"","osInfo":"","geoIp":""},"appUserId":"80931046","eventType":"custom","sessionId":6830887843,"playSessionId":6830887843,"platform":"ios","appVersion":"13.3.2","ip":"72.185.71.14","languageCode":"en_US","clientTimezoneOffset":-18000000,"raveId":"e16463baeeb548bb81afb696e83ce9fd","environment":"prod","appName":"casino","timestampClient":1639184399,"clientEventId":"3975853c-d629-4a3b-8c0b-1df240a24f32","bfgSdkVersion":"06090000","bfgudid":"0000000000000000000000000000000000000000","timestampServer":"","appBuildVersion":"","msgPayloadVersion":"","countryCode":""}'
```

```
curl -X 'POST' \
  'http://127.0.0.1/server_event/?appId=slotzilla&accountId=51961811&sessionId=6830853360&signature=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjp7ImV2ZW50RGF0YSI6eyJldmVudFR5cGUiOiJvbmJvYXJkaW5nIiwibG9hZF90aW1lIjo2NCwidHNfY2xpZW50X2RldmljZSI6MTYzOTE4NDQ1OSwidmFsdWUiOjEsInBsYXRmb3JtQWNjb3VudElkIjoxMTE1MTk0OTV9LCJkZXZpY2VJbmZvIjp7InRoaXJkUGFydHlUcmFja2luZ0VuYWJsZWQiOjAsImlmYSI6IjhDNjhFNkYxLTJFNUMtNEIxQy1CRjVBLUU1NTY1NzMwODJBNyIsImFwcFRyYWNraW5nVHJhbnNwYXJlbmN5U3RhdHVzIjoiMCIsImlmYUVuYWJsZWQiOjF9LCJldmVudE5hbWUiOiJzYWtpdF9zdGFydGVkIiwiZGV2aWNlTW9kZWwiOiJpUGFkIiwib3NWZXJzaW9uIjoiMTQuNC4yIiwic2NyZWVuUmVzb2x1dGlvbiI6IjgxMHgxMDgwIiwiYnVuZGxlSWQiOiJjb20uYmlnZmlzaGdhbWVzLmphY2twb3RjaXR5c2xvdHNmMnBpb3MiLCJhcHBTdG9yZSI6IiIsImFwcFN0b3JlSWQiOiIiLCJkZXZpY2VCcmFuZCI6IiIsImRldmljZUNhcnJpZXIiOiIiLCJkZXZpY2VJZGlvbSI6IiIsInByb2Nlc3NvclR5cGUiOiIiLCJvc0luZm8iOiIiLCJnZW9JcCI6IiJ9LCJhcHBVc2VySWQiOiI1MTk2MTgxMSIsImV2ZW50VHlwZSI6ImN1c3RvbSIsInNlc3Npb25JZCI6NjgzMDg1MzM2MCwicGxheVNlc3Npb25JZCI6NjgzMDg1MzM2MCwicGxhdGZvcm0iOiJpb3MiLCJhcHBWZXJzaW9uIjoiMTMuMi4yIiwiaXAiOiIyMTMuMjA1LjE5Mi4yNDIiLCJsYW5ndWFnZUNvZGUiOiJlbl9HQiIsImNsaWVudFRpbWV6b25lT2Zmc2V0IjowLCJyYXZlSWQiOiJmOGVkMGZlNDRkMWY0MGQ3YjFkNWMwOTM3YTViYzA2YSIsImVudmlyb25tZW50IjoicHJvZCIsImFwcE5hbWUiOiJzbG90emlsbGEiLCJ0aW1lc3RhbXBDbGllbnQiOjE2MzkxODQ0NTksImNsaWVudEV2ZW50SWQiOiI5NzM5OWFiMC1jZWEyLTQzZWMtOGExMi1lYmJlMDEzNDkyOTkiLCJiZmdTZGtWZXJzaW9uIjoiMDYwOTAwMDAiLCJiZmd1ZGlkIjoiMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMCIsInRpbWVzdGFtcFNlcnZlciI6IiIsImFwcEJ1aWxkVmVyc2lvbiI6IiIsIm1zZ1BheWxvYWRWZXJzaW9uIjoiIiwiY291bnRyeUNvZGUiOiIifQ.jdWxIB0fw6YYQMcGno_ivRFw08kzm7_Q-nHKkxUlBal61GNBVoD-QIxuOtrMvhtKFxDKaCQvKWBB1OMupf4gBw' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"data":{"eventData":{"eventType":"onboarding","load_time":64,"ts_client_device":1639184459,"value":1,"platformAccountId":111519495},"deviceInfo":{"thirdPartyTrackingEnabled":0,"ifa":"8C68E6F1-2E5C-4B1C-BF5A-E556573082A7","appTrackingTransparencyStatus":"0","ifaEnabled":1},"eventName":"sakit_started","deviceModel":"iPad","osVersion":"14.4.2","screenResolution":"810x1080","bundleId":"com.bigfishgames.jackpotcityslotsf2pios","appStore":"","appStoreId":"","deviceBrand":"","deviceCarrier":"","deviceIdiom":"","processorType":"","osInfo":"","geoIp":""},"appUserId":"51961811","eventType":"custom","sessionId":6830853360,"playSessionId":6830853360,"platform":"ios","appVersion":"13.2.2","ip":"213.205.192.242","languageCode":"en_GB","clientTimezoneOffset":0,"raveId":"f8ed0fe44d1f40d7b1d5c0937a5bc06a","environment":"prod","appName":"slotzilla","timestampClient":1639184459,"clientEventId":"97399ab0-cea2-43ec-8a12-ebbe01349299","bfgSdkVersion":"06090000","bfgudid":"0000000000000000000000000000000000000000","timestampServer":"","appBuildVersion":"","msgPayloadVersion":"","countryCode":""}'
```

```
curl -X 'POST' \
  'http://127.0.0.1/server_event/?appId=casino&accountId=79839995&sessionId=6830788022&signature=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjp7ImV2ZW50RGF0YSI6eyJldmVudFR5cGUiOiJ2aWV3X21ldHJpY3MiLCJ2aWV3X3NldCI6ImRpcmVjdF9wdWJsaXNoIiwidmlld19uYW1lIjoiY2FzaW5vdGltZXJnZW5lcmljaGFwcHlob3Vyc2FsZTd4Iiwidmlld190aGVtZSI6ImRlZmF1bHQiLCJidXR0b25fbmFtZSI6ImNsb3NlIiwicHJvbW9faWQiOiIxMzY3OSIsInRzX2NsaWVudF9kZXZpY2UiOjE2MzkxODQ0NTQsInZhbHVlIjoxLCJwbGF0Zm9ybUFjY291bnRJZCI6MjA5NDkzMjQyfSwiZGV2aWNlSW5mbyI6eyJ0aGlyZFBhcnR5VHJhY2tpbmdFbmFibGVkIjoxLCJpZmEiOiIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDAiLCJhcHBUcmFja2luZ1RyYW5zcGFyZW5jeVN0YXR1cyI6IjIiLCJpZmFFbmFibGVkIjowfSwiZXZlbnROYW1lIjoiY2xpY2siLCJkZXZpY2VNb2RlbCI6ImlQYWQiLCJvc1ZlcnNpb24iOiIxNS4xIiwic2NyZWVuUmVzb2x1dGlvbiI6IjgzNHgxMTk0IiwiYnVuZGxlSWQiOiJjb20uYmlnZmlzaGdhbWVzLmJmY2FzaW5vdW5pdmVyc2FsZnJlZW1pdW0iLCJhcHBTdG9yZSI6IiIsImFwcFN0b3JlSWQiOiIiLCJkZXZpY2VCcmFuZCI6IiIsImRldmljZUNhcnJpZXIiOiIiLCJkZXZpY2VJZGlvbSI6IiIsInByb2Nlc3NvclR5cGUiOiIiLCJvc0luZm8iOiIiLCJnZW9JcCI6IiJ9LCJhcHBVc2VySWQiOiI3OTgzOTk5NSIsImV2ZW50VHlwZSI6ImN1c3RvbSIsInNlc3Npb25JZCI6NjgzMDc4ODAyMiwicGxheVNlc3Npb25JZCI6NjgzMDc4ODAyMiwicGxhdGZvcm0iOiJpb3MiLCJhcHBWZXJzaW9uIjoiMTMuMy4wIiwiaXAiOiI3My41OS45Ni4yMTciLCJsYW5ndWFnZUNvZGUiOiJlbl9VUyIsImNsaWVudFRpbWV6b25lT2Zmc2V0IjotMjg4MDAwMDAsInJhdmVJZCI6IjYzMzJlODk0YzU4OTRjMGE4ZTljOGRmNmMwOTQ3MWQ5IiwiZW52aXJvbm1lbnQiOiJwcm9kIiwiYXBwTmFtZSI6ImNhc2lubyIsInRpbWVzdGFtcENsaWVudCI6MTYzOTE4NDQ1OSwiY2xpZW50RXZlbnRJZCI6Ijc5NjU4NzExLTVkNDUtNGFlNy04MDc3LTM2MmVhYmM1M2ZmMyIsImJmZ1Nka1ZlcnNpb24iOiIwNjA5MDAwMCIsImJmZ3VkaWQiOiIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIiwidGltZXN0YW1wU2VydmVyIjoiIiwiYXBwQnVpbGRWZXJzaW9uIjoiIiwibXNnUGF5bG9hZFZlcnNpb24iOiIiLCJjb3VudHJ5Q29kZSI6IiJ9.ZQW5N6yFmGj3VLLvE97C4TcYIGrOTxJIsHaYsvhdNRjuGQ23B91juEC4ednsDfguuSHnkZWE9G1Z0BXQ-twh0A' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"data":{"eventData":{"eventType":"view_metrics","view_set":"direct_publish","view_name":"casinotimergenerichappyhoursale7x","view_theme":"default","button_name":"close","promo_id":"13679","ts_client_device":1639184454,"value":1,"platformAccountId":209493242},"deviceInfo":{"thirdPartyTrackingEnabled":1,"ifa":"00000000-0000-0000-0000-000000000000","appTrackingTransparencyStatus":"2","ifaEnabled":0},"eventName":"click","deviceModel":"iPad","osVersion":"15.1","screenResolution":"834x1194","bundleId":"com.bigfishgames.bfcasinouniversalfreemium","appStore":"","appStoreId":"","deviceBrand":"","deviceCarrier":"","deviceIdiom":"","processorType":"","osInfo":"","geoIp":""},"appUserId":"79839995","eventType":"custom","sessionId":6830788022,"playSessionId":6830788022,"platform":"ios","appVersion":"13.3.0","ip":"73.59.96.217","languageCode":"en_US","clientTimezoneOffset":-28800000,"raveId":"6332e894c5894c0a8e9c8df6c09471d9","environment":"prod","appName":"casino","timestampClient":1639184459,"clientEventId":"79658711-5d45-4ae7-8077-362eabc53ff3","bfgSdkVersion":"06090000","bfgudid":"0000000000000000000000000000000000000000","timestampServer":"","appBuildVersion":"","msgPayloadVersion":"","countryCode":""}'
```

Just copy and paste these commands to your terminal window. Response will be the following message:

```
{"status":"Event Successfully Sent"}
```

After you can visit Google Cloud Console,choose Pub/Sub and select topic that you specified for sending events.
![google pub/sub](https://i.ibb.co/xzk9qNq/pubsub-example.png  "google pub/sub screenshot")
What about queries where the signatures do not match? Let's check it out!
These are queries where the signatures match

```
curl -X 'POST' \
'http://127.0.0.1/server_event/?appId=casino&accountId=83247435&sessionId=6830888418&signature=kadhjf214r89123jd1982y3fdj1uhed17324676dfh1je287dj192e8udf1j34fug476t12gfeu1ehsjfkh8497746ryfeh17gewsjdhkslnqfciruyy7t14365r189h2ednesjk1bfy174356' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"data":{"eventData":{"eventType":"clubs","ts_client_device":1639184450,"value":1,"platformAccountId":220750481},"deviceInfo":{"thirdPartyTrackingEnabled":1,"ifa":"00000000-0000-0000-0000-000000000000","appTrackingTransparencyStatus":"2","ifaEnabled":0},"eventName":"bonus_page","deviceModel":"iPhone","osVersion":"15.1","screenResolution":"375x667","bundleId":"com.bigfishgames.bfcasinouniversalfreemium","appStore":"","appStoreId":"","deviceBrand":"","deviceCarrier":"","deviceIdiom":"","processorType":"","osInfo":"","geoIp":""},"appUserId":"83247435","eventType":"custom","sessionId":6830888418,"playSessionId":6830888418,"platform":"ios","appVersion":"13.2.6","ip":"68.34.20.242","languageCode":"en_US","clientTimezoneOffset":-18000000,"raveId":"1e232be66e924155b0e24046bb60648b","environment":"prod","appName":"casino","timestampClient":1639184459,"clientEventId":"3e4989f6-fc8a-4c2b-8306-70127d98e0ea","bfgSdkVersion":"06090000","bfgudid":"0000000000000000000000000000000000000000","timestampServer":"","appBuildVersion":"","msgPayloadVersion":"","countryCode":""}'
```

```
curl -X 'POST' \
'http://127.0.0.1/server_event/?appId=casino&accountId=23113599&sessionId=6830888970&signature=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjp7ImV2ZW50RGF0YSI6eyJldmVudFR5cGUiOiJjbHVicyIsImZpcnN0X3RpbWVfbG9naW4iOm51bGwsInRpbWVfc2luY2Vfc3RhcnQiOm51bGwsInZhbHVlIjoxLCJwbGF0Zm9ybUFjY291bnRJZCI6MjIwNzUwNDgxfSwiZGV2aWNlSW5mbyI6eyJ0aGlyZFBhcnR5VHJhY2tpbmdFbmFibGVkIjoxLCJpZmEiOiIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDAiLCJhcHBUcmFja2luZ1RyYW5zcGFyZW5jeVN0YXR1cyI6IjIiLCJpZmFFbmFibGVkIjowfSwiZXZlbnROYW1lIjoiYm9udXNfcGFnZSIsImRldmljZU1vZGVsIjoiaVBob25lIiwib3NWZXJzaW9uIjoiMTUuMSIsInNjcmVlblJlc29sdXRpb24iOiIzNzV4NjY3IiwiYnVuZGxlSWQiOiJjb20uYmlnZmlzaGdhbWVzLmJmY2FzaW5vdW5pdmVyc2FsZnJlZW1pdW0iLCJhcHBTdG9yZSI6IiIsImFwcFN0b3JlSWQiOiIiLCJkZXZpY2VCcmFuZCI6IiIsImRldmljZUNhcnJpZXIiOiIiLCJkZXZpY2VJZGlvbSI6IiIsInByb2Nlc3NvclR5cGUiOiIiLCJvc0luZm8iOiIiLCJnZW9JcCI6IiJ9LCJhcHBVc2VySWQiOiI4MzI0NzQzNSIsImV2ZW50VHlwZSI6ImN1c3RvbSIsInNlc3Npb25JZCI6NjgzMDg4ODQxOCwicGxheVNlc3Npb25JZCI6NjgzMDg4ODQxOCwicGxhdGZvcm0iOiJpb3MiLCJhcHBWZXJzaW9uIjoiMTMuMi42IiwiaXAiOiI2OC4zNC4yMC4yNDIiLCJsYW5ndWFnZUNvZGUiOiJlbl9VUyIsImNsaWVudFRpbWV6b25lT2Zmc2V0IjotMTgwMDAwMDAsInJhdmVJZCI6IjFlMjMyYmU2NmU5MjQxNTViMGUyNDA0NmJiNjA2NDhiIiwiZW52aXJvbm1lbnQiOiJwcm9kIiwiYXBwTmFtZSI6ImNhc2lubyIsInRpbWVzdGFtcENsaWVudCI6MTYzOTE4NDQ1OSwiY2xpZW50RXZlbnRJZCI6IjNlNDk4OWY2LWZjOGEtNGMyYi04MzA2LTcwMTI3ZDk4ZTBlYSIsImJmZ1Nka1ZlcnNpb24iOiIwNjA5MDAwMCIsImJmZ3VkaWQiOiIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIiwidGltZXN0YW1wU2VydmVyIjoiIiwiYXBwQnVpbGRWZXJzaW9uIjoiIiwibXNnUGF5bG9hZFZlcnNpb24iOiIiLCJjb3VudHJ5Q29kZSI6IiJ9.qXqdOvXtGIXK9uX4Sl_8gPRYDXqpnELHtLoIndbocsn42cIdFp7RC_KGefKpSnS4NJ403h2Ovuca20D5P4rJDQ' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"data":{"eventData":{"eventType":"view_metrics","view_set":"direct_publish","view_name":"casinotimergenerichappyhoursale7x","view_theme":"default","promo_id":"13679","ts_client_device":1639184450,"value":1,"platformAccountId":217786726},"deviceInfo":{"thirdPartyTrackingEnabled":1,"ifa":"00000000-0000-0000-0000-000000000000","appTrackingTransparencyStatus":"2","ifaEnabled":0},"eventName":"load","deviceModel":"iPhone","osVersion":"15.1","screenResolution":"375x667","bundleId":"com.bigfishgames.bfcasinouniversalfreemium","appStore":"","appStoreId":"","deviceBrand":"","deviceCarrier":"","deviceIdiom":"","processorType":"","osInfo":"","geoIp":""},"appUserId":"23113599","eventType":"custom","sessionId":6830888970,"playSessionId":6830888970,"platform":"ios","appVersion":"13.2.6","ip":"68.11.171.128","languageCode":"en_US","clientTimezoneOffset":-21600000,"raveId":"25d10044338b4b0fb3efa427507cd881","environment":"prod","appName":"casino","timestampClient":1639184459,"clientEventId":"26cc349f-1af3-45a7-89df-a751c02a26a1","bfgSdkVersion":"06090000","bfgudid":"0000000000000000000000000000000000000000","timestampServer":"","appBuildVersion":"","msgPayloadVersion":"","countryCode":""}'
```

```
curl -X 'POST' \
'http://127.0.0.1/server_event/?appId=casino&accountId=7145507&sessionId=6830813570&signature=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjp7ImV2ZW50RGF0YSI6eyJldmVudFR5cGUiOiJ2aWV3X21ldHJpY3MiLCJmaXJzdF90aW1lX2xvZ2luIjpudWxsLCJ0aW1lX3NpbmNlX3N0YXJ0IjpudWxsLCJ2YWx1ZSI6MSwicGxhdGZvcm1BY2NvdW50SWQiOjIwOTQ5MzI0Mn0sImRldmljZUluZm8iOnsidGhpcmRQYXJ0eVRyYWNraW5nRW5hYmxlZCI6MSwiaWZhIjoiMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwIiwiYXBwVHJhY2tpbmdUcmFuc3BhcmVuY3lTdGF0dXMiOiIyIiwiaWZhRW5hYmxlZCI6MH0sImV2ZW50TmFtZSI6ImNsaWNrIiwiZGV2aWNlTW9kZWwiOiJpUGFkIiwib3NWZXJzaW9uIjoiMTUuMSIsInNjcmVlblJlc29sdXRpb24iOiI4MzR4MTE5NCIsImJ1bmRsZUlkIjoiY29tLmJpZ2Zpc2hnYW1lcy5iZmNhc2lub3VuaXZlcnNhbGZyZWVtaXVtIiwiYXBwU3RvcmUiOiIiLCJhcHBTdG9yZUlkIjoiIiwiZGV2aWNlQnJhbmQiOiIiLCJkZXZpY2VDYXJyaWVyIjoiIiwiZGV2aWNlSWRpb20iOiIiLCJwcm9jZXNzb3JUeXBlIjoiIiwib3NJbmZvIjoiIiwiZ2VvSXAiOiIifSwiYXBwVXNlcklkIjoiNzk4Mzk5OTUiLCJldmVudFR5cGUiOiJjdXN0b20iLCJzZXNzaW9uSWQiOjY4MzA3ODgwMjIsInBsYXlTZXNzaW9uSWQiOjY4MzA3ODgwMjIsInBsYXRmb3JtIjoiaW9zIiwiYXBwVmVyc2lvbiI6IjEzLjMuMCIsImlwIjoiNzMuNTkuOTYuMjE3IiwibGFuZ3VhZ2VDb2RlIjoiZW5fVVMiLCJjbGllbnRUaW1lem9uZU9mZnNldCI6LTI4ODAwMDAwLCJyYXZlSWQiOiI2MzMyZTg5NGM1ODk0YzBhOGU5YzhkZjZjMDk0NzFkOSIsImVudmlyb25tZW50IjoicHJvZCIsImFwcE5hbWUiOiJjYXNpbm8iLCJ0aW1lc3RhbXBDbGllbnQiOjE2MzkxODQ0NTksImNsaWVudEV2ZW50SWQiOiI3OTY1ODcxMS01ZDQ1LTRhZTctODA3Ny0zNjJlYWJjNTNmZjMiLCJiZmdTZGtWZXJzaW9uIjoiMDYwOTAwMDAiLCJiZmd1ZGlkIjoiMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMCIsInRpbWVzdGFtcFNlcnZlciI6IiIsImFwcEJ1aWxkVmVyc2lvbiI6IiIsIm1zZ1BheWxvYWRWZXJzaW9uIjoiIiwiY291bnRyeUNvZGUiOiIifQ.H550C8hJga-OMzWBY2rQeTgMrrAuFK3d6GqJmVvL8bLS3Bb8xDuFIiT7wKk4vs1m8s3CLoAbd70uG-uj33-plA' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"data":{"eventData":{"eventType":"view_metrics","view_set":"direct_publish","view_name":"casinotimergenerichappyhoursale7x","view_theme":"default","promo_id":"13679","ts_client_device":1639184450,"value":1,"platformAccountId":180492816},"deviceInfo":{"thirdPartyTrackingEnabled":1,"ifa":"4A116431-3641-46D7-AEC5-C796B8B2F7E2","appTrackingTransparencyStatus":"3","ifaEnabled":0},"eventName":"load","deviceModel":"iPhone","osVersion":"15.1.1","screenResolution":"375x812","bundleId":"com.bigfishgames.bfcasinouniversalfreemium","appStore":"","appStoreId":"","deviceBrand":"","deviceCarrier":"","deviceIdiom":"","processorType":"","osInfo":"","geoIp":""},"appUserId":"7145507","eventType":"custom","sessionId":6830813570,"playSessionId":6830813570,"platform":"ios","appVersion":"13.2.6","ip":"50.100.98.224","languageCode":"en_CA","clientTimezoneOffset":-18000000,"raveId":"c2362209d73243da94d7c17c84401f82","environment":"prod","appName":"casino","timestampClient":1639184460,"clientEventId":"bcd5f3f9-fe36-4eb9-8721-482e8326f665","bfgSdkVersion":"06090000","bfgudid":"0000000000000000000000000000000000000000","timestampServer":"","appBuildVersion":"","msgPayloadVersion":"","countryCode":""}'
```

Just copy and paste these commands to your terminal window. The API collect butch of 20 requests with bad signatures and
send message via Slack bot. Response will be an exception with the following message:

```
"detail":"Signatures didn't Match"
```

After that, let's go to check our Slack! And we can see the following messages from our Bot:
![slack example](https://i.ibb.co/MpwzqDM/Screen-Shot-2022-01-21-at-15-27-00.png "slack example screenshot")

## :punch: Unit Tests :punch:

You need a file with event examples for testing

- Create `setenv.sh` file and add it in you root project directory
- In `setenv.sh` specify environment variables:

```
export KEY=<your_secret_key_for_encrypting>
export SLACK_BOT_TOKEN=<your_slack_bot_token>
export CHANNEL_ID=<your_slack_channel_id>
export GCP_PROJECT_ID=<your_gcp_project_id>
export GCP_TOPIC_ID=<your_gcp_pub_sub_topic_id>
export PATH_TO_EVENT_DATA_FOR_TEST="<path_to_you_event_data_for_test>"
export GOOGLE_APPLICATION_CREDENTIALS="/<path_to_your_gcp_credentials_json_file>/<your_gcp_credentials_json_file.json>
```

- export your environment variables. Go to your project root directory and in terminal window, enter:

```
source ./setenv
```

- Create and activate virtual environment for this project
- Install the dependencies from `requirements.txt` file
- In terminal window, enter:

```
pytest
```

When unit testing is finished you will see a report:
![pytest report](https://i.ibb.co/7jhRt2g/pytest-report.png "pytest report screenshot")

## :mag: Interactive API docs :mag:

Now you can go to  [http://192.168.99.100/docs](http://192.168.99.100/docs)
or  [http://127.0.0.1/docs](http://127.0.0.1/docs)  (or equivalent, using your Docker host). You will see the automatic
interactive API documentation (provided by  [Swagger UI](https://github.com/swagger-api/swagger-ui)):
![swagger ui](https://i.ibb.co/rMHWz3f/swagger-example.png "swagger UI screenshot")

### :feelsgood: :feelsgood: :feelsgood: Everything is working :feelsgood: :feelsgood: :feelsgood: