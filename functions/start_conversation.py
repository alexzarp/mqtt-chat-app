from functions.publish import publish
from functions.subscribe import subscribe, unsubscribe
import json
from paho.mqtt import client as mqtt_client
from data._globals import *


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


def send_message(client_mqtt: mqtt_client.Client):
    print("Usuarios conectados: ", end="\n")
    for i in range(len(topics)):
        print(f"{i} - {topics[i]}")
    print()

    print("Escolha o tópico: \n>>> ", end="")
    topic = str(input())

    print("Digite a mensagem: \n>>> ", end="")
    message = str(input())

    publish(
        client_mqtt,
        topic,
        json.dumps(
            {
                "action": "message",
                "message": message,
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
