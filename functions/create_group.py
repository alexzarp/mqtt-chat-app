from paho.mqtt import client as mqtt_client
from functions.publish import publish
from functions.subscribe import subscribe
from handle_comunication.handle_comunication import displaymsgfromgroups
import json
from data._globals import *


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
                "name": name,
                "leader": (mqtt_client._client_id).decode("utf-8"),
            },
        ),
    )

    # groups[(mqtt_client._client_id).decode("utf-8")] = name

    print(
        f"Criando o grupo `{name}` em que o meu usário \
`{(mqtt_client._client_id).decode('utf-8')}` é o líder.",
        end="\n\n",
    )

    subscribe(
        client_mqtt=mqtt_client,
        topic=name,
        on_message=displaymsgfromgroups,
    )


def join_group(mqtt_client: mqtt_client.Client):
    print("Digite o nome do grupo solicitar entrada: \n>>> ", end="")
    name = str(input())
    print()

    publish(
        mqtt_client,
        "groups",
        json.dumps(
            {
                "action": "join_group",
                "name": name,
                "client": (mqtt_client._client_id).decode("utf-8"),
            },
        ),
    )

    print(f"Solicitando entrada no grupo `{name}`", end="\n\n")
