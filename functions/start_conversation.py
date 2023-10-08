from functions.publish import publish
from functions.subscribe import subscribe
import json

def start_conversation(client_mqtt, topic, message):
    publish(client_mqtt, topic, json.dumps({"action": "coversation"}))

    publish(client_mqtt, "topic", "msg")