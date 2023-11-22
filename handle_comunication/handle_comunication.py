from paho.mqtt import client as mqtt_client
import redis
from functions.publish import publish
import json

redis = redis.Redis()


def display_message(client, message):
    print(f"Mensagem de {client}: {message}")


def monitor(mqtt_client: mqtt_client.Client, userdata, msg):
    import json

    json = json.loads(msg.payload.decode())
    user = json["user"]

    redis.set(f"global_control: {user}", json)


def mytopic(mqtt_client: mqtt_client.Client, userdata, msg):
    import json

    json = json.loads(msg.payload.decode())

    match json["action"]:
        case "conversation":
            client = json["client"]
            if json["message"] == (mqtt_client._client_id).decode("utf-8"):
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

        case "accept":
            client = json["client"]
            if json["message"] == (mqtt_client._client_id).decode("utf-8"):
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
