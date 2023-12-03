from paho.mqtt import client as mqtt_client
from functions.publish import publish
from functions.subscribe import subscribe, unsubscribe
import json
from threading import Thread
from data._globals import *
from pynput.keyboard import Key, Controller
from time import sleep


def monitor(mqtt_client: mqtt_client.Client, userdata, msg):
    import json

    recv = json.loads(msg.payload.decode())
    user = recv["user"]
    status = recv["status"]

    local = None
    try:
        with open("data/storage.json", "+r") as arquivo:
            local = json.load(arquivo)
    except:  # arquivo vazio
        local = {f"{user}": {"status": status}}
        with open("data/storage.json", "+w") as arquivo:
            json.dump(local, arquivo, indent=4)

    saved_user = local.get(f"{user}")
    if saved_user is None:
        local[f"{user}"] = {"status": status}
    else:
        local[f"{user}"]["status"] = status

    with open("data/storage.json", "+r") as arquivo:
        json.dump(local, arquivo, indent=4)


def mytopic(mqtt_client: mqtt_client.Client, userdata, msg):
    import json
    import datetime

    recv = json.loads(msg.payload.decode())

    print(recv)

    match recv["action"]:
        case "conversation":
            client = recv["client"]
            temp_topic = (
                (mqtt_client._client_id).decode("utf-8") + client + "_conversation"
            )

            publish(
                mqtt_client,
                client + "_control",
                json.dumps(
                    {
                        "action": "accept",
                        "message": temp_topic,
                        "client": (mqtt_client._client_id).decode("utf-8"),
                    },
                ),
            )
            topics[client] = temp_topic
            subscribe(
                client_mqtt=mqtt_client,
                topic=temp_topic,
                on_message=displaymsg,
            )
            print(f"Conversa com {client} iniciada no {temp_topic}.\n")

        case "accept":
            client = recv["client"]
            temp_topic = recv["message"]
            print(f"Conversa com {client} iniciada no {temp_topic}.\n")
            topics[client] = temp_topic
            subscribe(
                client_mqtt=mqtt_client,
                topic=temp_topic,
                on_message=displaymsg,
            )

        case _:
            print(f"Erro: {recv}")


def conversation(mqtt_client: mqtt_client.Client, temp_topic):
    print("Digite a mensagem: \n>>> ", end="")
    message = str(input())
    publish(
        mqtt_client,
        temp_topic,
        json.dumps(
            {
                "action": "message",
                "message": message,
                "client": (mqtt_client._client_id).decode("utf-8"),
            },
        ),
    )

    publish(
        mqtt_client,
        temp_topic,
        json.dumps(
            {
                "action": "exit",
                "message": temp_topic,
                "client": (mqtt_client._client_id).decode("utf-8"),
            },
        ),
    )
    unsubscribe(mqtt_client, temp_topic)


def displaymsg(mqtt_client: mqtt_client.Client, userdata, msg):
    message = json.loads(msg.payload.decode())

    if message.get("action") == "exit":
        unsubscribe(mqtt_client, message["topic"])
        print(f"`{message['client']}` encerrou a conversa `{message['topic']}`")
        topics.pop(message["client"])

    if (
        message["client"] != (mqtt_client._client_id).decode("utf-8")
        and message.get("message") != None
    ):
        print(
            f"Mensagem de {(mqtt_client._client_id).decode('utf-8')}: {message['message']}\n"
        )
