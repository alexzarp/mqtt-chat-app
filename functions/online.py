from functions.publish import publish
from paho.mqtt import client as mqtt_client
import json
from time import sleep


def online(mqtt_client: mqtt_client.Client, topic="users", online=True):
    payload = {
        "status": "online" if online else "offline",
        "user": (mqtt_client._client_id).decode("utf-8"),
    }
    publish(
        mqtt_client=mqtt_client,
        topic=topic,
        payload=json.dumps(payload),  # .encode("utf-8"),
    )
