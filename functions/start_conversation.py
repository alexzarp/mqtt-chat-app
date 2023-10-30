from functions.publish import publish
from functions.subscribe import subscribe
import json


def start_conversation(client_mqtt, topic, message):
    publish(
        client_mqtt,
        topic + "_control",
        json.dumps(
            {
                "action": "coversation",
                "message": message,
                "client": client_mqtt._client_id,
            },
        ),
    )