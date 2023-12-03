from paho.mqtt import client as mqtt_client
from functions.publish import publish
from functions.subscribe import subscribe
from handle_comunication.handle_comunication import displaymsgfromgroups
import json


def create_group(mqtt_client: mqtt_client.Client):
    print("Digite o nome do grupo a ser criado: \n>>> ", end="")
    name = str(input())
    print()

    publish(
        mqtt_client,
        "groups",
        json.dumps(
            {
                "action": "create_group",
                "message": name,
                "leader": (mqtt_client._client_id).decode("utf-8"),
            },
        ),
    )

    subscribe(
        client_mqtt=mqtt_client,
        topic=name,
        on_message=displaymsgfromgroups,
    )
