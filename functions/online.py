from functions.publish import publish
import json
from time import sleep


def online(client_mqtt, topic="global_control"):
    payload = json.loads(
        '{"client": {}}'.format(
            client_mqtt._client_id,
        )
    )
    while 1:
        publish(
            client_mqtt=client_mqtt,
            topic=topic,
            payload=payload,
        )
        sleep(2)
