from google.cloud import pubsub_v1

from app.config import GCP_PROJECT_ID, GCP_TOPIC_ID


def send_message_to_pub_sub_topic(message):

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(GCP_PROJECT_ID, GCP_TOPIC_ID)

    data = message
    # Data must be a bytestring
    data = data.encode("utf-8")
    # Add two attributes, origin and username, to the message
    future = publisher.publish(
        topic_path, data, origin="python-sample", username="gcp"
    )
