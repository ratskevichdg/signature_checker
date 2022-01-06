import os

from google.cloud import pubsub_v1


def send_message_to_pub_sub_topic(message):

    GCP_PROJECT_ID = os.environ['GCP_PROJECT_ID']
    GCP_TOPIC_ID = os.environ['GCP_TOPIC_ID']

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(GCP_PROJECT_ID, GCP_TOPIC_ID)

    data = message
    # Data must be a bytestring
    data = data.encode("utf-8")
    # Add two attributes, origin and username, to the message
    future = publisher.publish(
        topic_path, data, origin="python-sample", username="gcp"
    )
    print(future.result())

    print(f"Published messages with custom attributes to {topic_path}.")
