from functions.publish import publish
import json
from time import sleep


def online(client_mqtt, topic="global_control", online=True):
    publish(
        client_mqtt=client_mqtt,
        topic="global_control",
        payload={
            "status": "online" if online else "offline",
            "user": client_mqtt._client_id,
        },
    )
