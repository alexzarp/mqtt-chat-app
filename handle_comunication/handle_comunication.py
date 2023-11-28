from paho.mqtt import client as mqtt_client
from functions.publish import publish
from functions.subscribe import subscribe
import json
from threading import Thread


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

    recv = json.loads(msg.payload.decode())
    match recv["action"]:
        case "conversation":
            client = recv["client"]
            temp_topic = (
                (mqtt_client._client_id).decode("utf-8") + client + "_timestamp"
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
            subscribe(
                client_mqtt=mqtt_client,
                topic=temp_topic,
                on_message=displaymsg,
            )

        case "accept":
            client = recv["client"]
            temp_topic = recv["message"]
            print(
                f"Conversa com {client} iniciada. Digite `\exit` para sair deste chat."
            )
            t = Thread(target=conversation, args=(mqtt_client, temp_topic))
            t.start()

        case "exit":
            mqtt_client.unsubscribe(temp_topic)


def conversation(mqtt_client: mqtt_client.Client, temp_topic):
    subscribe(
        client_mqtt=mqtt_client,
        topic=temp_topic,
        on_message=displaymsg,
    )
    while 1:
        message = input("Digite a mensagem: \n>>>")
        if message == "\exit":
            break

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
    mqtt_client.unsubscribe(temp_topic)


()


def displaymsg(mqtt_client: mqtt_client.Client, userdata, msg):
    print(f"Mensagem de {(mqtt_client._client_id).decode('utf-8')}: {msg}")
