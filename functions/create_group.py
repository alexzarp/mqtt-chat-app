from paho.mqtt import client as mqtt_client
from functions.publish import publish
import json


def create_group(mqtt_client: mqtt_client.Client):
    publish(
        mqtt_client,
        "global_control",
        json.dumps(
            {
                "action": "create_group",
                "message": "group_name",
                "client": (mqtt_client._client_id).decode("utf-8"),
            },
        ),
    )
