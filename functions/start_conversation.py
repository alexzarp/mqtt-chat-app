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
    print("User - Topic")
    for i in topics.keys():
        print(f"{i} - {topics[i]}")
    print()

    print("Escolha o usuario: \n>>> ", end="")
    topic = str(input())
    try:
        topic = topics[topic]
    except:
        print(f"Usuario {topic} não encontrado")
        return

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


def send_message_group(client_mqtt: mqtt_client.Client):
    pass


def end_conversation(client_mqtt: mqtt_client.Client):
    print("Usuarios conectados: ", end="\n")
    print("User - Topic")
    for i in topics.keys():
        print(f"{i} - {topics[i]}")
    print()

    print("Escolha o usuario para encerrar: \n>>> ", end="")
    topic = str(input())
    try:
        _topic = topics[topic]
    except:
        print(f"Usuario {topic} não encontrado")
        return

    publish(
        client_mqtt,
        topics.get(topic),
        json.dumps(
            {
                "action": "exit",
                "topic": topics.get(topic),
                "client": (client_mqtt._client_id).decode("utf-8"),
            },
        ),
    )

    print(f"Encerrado a conversa no `{_topic}`")
    unsubscribe(client_mqtt, _topic)
    topics.pop(topic)
    return "stand"
