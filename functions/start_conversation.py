from functions.publish import publish
from functions.subscribe import subscribe
import json
from paho.mqtt import client as mqtt_client


def start_conversation(client_mqtt: mqtt_client.Client, topic, message):
    publish(
        client_mqtt,
        topic + "_control",
        json.dumps(
            {
                "action": "coversation",
                "message": message,
                "client": (client_mqtt._client_id).decode("utf-8"),
            },
        ),
    )
