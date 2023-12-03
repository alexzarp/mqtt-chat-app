from paho.mqtt import client as mqtt_client
from functions.publish import publish
from functions.subscribe import subscribe, unsubscribe
import json
from threading import Thread
from data._globals import *
from pynput.keyboard import Key, Controller
from time import sleep


def monitor(mqtt_client: mqtt_client.Client, userdata, msg):
    recv = json.loads(msg.payload.decode())
    user = recv["user"]
    status = recv["status"]

    try:
        with open("data/storage.json", "r") as arquivo:
            local = json.load(arquivo)
    except FileNotFoundError:  # Se o arquivo não existir
        local = {f"{user}": {"status": status}}
    except json.JSONDecodeError:  # Se o arquivo estiver vazio ou com formato inválido
        local = {f"{user}": {"status": status}}
    else:
        saved_user = local.get(f"{user}")
        if saved_user is None:
            local[f"{user}"] = {"status": status}
        else:
            local[f"{user}"]["status"] = status

    with open("data/storage.json", "w") as arquivo:
        json.dump(local, arquivo, indent=4)


def mytopic(mqtt_client: mqtt_client.Client, userdata, msg):
    import json
    import datetime

    recv = json.loads(msg.payload.decode())

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

        case "mygroup":
            client = recv["leader"]
            name = recv["name"]
            print(f"Entrei no grupo `{name}` onde `{client}` é líder.\n")

            subscribe(
                client_mqtt=mqtt_client,
                topic=name,
                on_message=displaymsgfromgroups,
            )

            save_joined_groups(mqtt_client, recv)

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

    if message.get("action") == "exit" and message.get("client") != (
        mqtt_client._client_id
    ).decode("utf-8"):
        unsubscribe(mqtt_client, message["topic"])
        print(
            f"`{message['client']}` encerrou a conversa `{message['topic']}`",
            end="\n\n",
        )
        print(topics)
        topics.pop(message["client"])

    if (
        message["client"] != (mqtt_client._client_id).decode("utf-8")
        and message.get("message") != None
    ):
        print(f"Mensagem de {message['client']}: {message['message']}\n")


def displaymsgfromgroups(mqtt_client: mqtt_client.Client, userdata, msg):
    message = json.loads(msg.payload.decode())
    if (
        message["client"] != (mqtt_client._client_id).decode("utf-8")
        and message.get("message") != None
    ):
        print(
            f"Mensagem de `{message['client']}` no grupo `{message['group']}`: {message['message']}\n"
        )


def susbscribe_lasts(client_mqtt: mqtt_client.Client):
    import json

    try:
        with open(
            f"data/{(client_mqtt._client_id).decode('utf-8')}_groups.json", "r"
        ) as f:
            lasts = json.load(f)
    except:
        return

    for i, j in lasts.items():
        subscribe(client_mqtt, j["name"], displaymsgfromgroups)


def save_joined_groups(mqtt_client: mqtt_client.Client, recv):
    leader = recv["leader"]
    name = recv["name"]
    try:
        with open(
            f"data/{(mqtt_client._client_id).decode('utf-8')}_groups.json", "r"
        ) as arquivo:
            local = json.load(arquivo)
    except FileNotFoundError:  # Se o arquivo não existir
        local = {f"{leader}": {"name": name}}
    except json.JSONDecodeError:  # Se o arquivo estiver vazio ou com formato inválido
        local = {f"{leader}": {"name": name}}
    else:
        saved_user = local.get(f"{leader}")
        if saved_user is None:
            local[f"{leader}"] = {"name": name}
        else:
            local[f"{leader}"]["name"] = name
    with open(
        f"data/{(mqtt_client._client_id).decode('utf-8')}_groups.json", "w"
    ) as arquivo:
        json.dump(local, arquivo, indent=4)


def groups_handle(mqtt_client: mqtt_client.Client, userdata, msg):
    import json
    import datetime

    recv = json.loads(msg.payload.decode())

    match recv["action"]:
        case "create_group":
            if recv["leader"] != (mqtt_client._client_id).decode("utf-8"):
                return
            save_joined_groups(mqtt_client, recv)

            print(
                f"Criado o grupo `{recv['name']}` em que `{(mqtt_client._client_id).decode('utf-8')}` é o líder.",
                end="\n\n",
            )

        case "join_group":
            client = recv["client"]
            name = recv["name"]

            try:
                with open(
                    f"data/{(mqtt_client._client_id).decode('utf-8')}_groups.json", "r"
                ) as arquivo:
                    local = json.load(arquivo)
            except:  # Se o arquivo não existir
                return

            for i in local.keys():
                if local[i]["name"] == name and i == (mqtt_client._client_id).decode(
                    "utf-8"
                ):
                    publish(
                        mqtt_client,
                        client + "_control",
                        json.dumps(
                            {
                                "action": "mygroup",
                                "name": name,
                                "leader": (mqtt_client._client_id).decode("utf-8"),
                            },
                        ),
                    )
                    print(f"Aceitei `{i}` no meu grupo `{name}`", end="\n\n")

        case _:
            print(f"Erro: {recv}")
