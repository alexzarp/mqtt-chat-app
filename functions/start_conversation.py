from functions.publish import publish
from functions.subscribe import subscribe, unsubscribe
import json
from paho.mqtt import client as mqtt_client


def start_conversation(client_mqtt: mqtt_client.Client, topic):
    publish(
        client_mqtt,
        topic + "_control",
        json.dumps(
            {
                "action": "conversation",
                "client": (client_mqtt._client_id).decode("utf-8"),
            },
        ),
    )
    return "stand"


def end_conversation(client_mqtt: mqtt_client.Client, topic):
    publish(
        client_mqtt,
        topic,
        json.dumps(
            {
                "action": "exit",
                "topic": topic,
                "client": (client_mqtt._client_id).decode("utf-8"),
            },
        ),
    )
    unsubscribe(client_mqtt, topic)
    return "stand"
