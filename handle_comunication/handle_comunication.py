from paho.mqtt import client as mqtt_client
from functions.publish import publish
import json


def display_message(client, message):
    print(f"Mensagem de {client}: {message}")


def monitor(mqtt_client: mqtt_client.Client, userdata, msg):
    import json

    recv = json.loads(msg.payload.decode())

    local = None
    with open("data/storage.json", "r+") as arquivo:
        local = json.load(arquivo)

    print(local)
    user = recv["user"]
    status = recv["status"]

    saved_user = local.get(f"{user}")
    if saved_user is None:
        local[f"{user}"] = {"status": status}
    else:
        local[f"{user}"]["status"] = status

    with open("data/storage.json", "r") as arquivo:
        json.dump(local, arquivo, indent=4)


# def mytopic(mqtt_client: mqtt_client.Client, userdata, msg):
#     import json

#     json = json.loads(msg.payload.decode())

#     print("OIIIIIIIIi", json)
#     match json["action"]:
#         case "conversation":
#             client = json["client"]
#             if json["message"] == (mqtt_client._client_id).decode("utf-8"):
#                 temp_topic = (
#                     (mqtt_client._client_id).decode("utf-8") + client + "_timestamp"
#                 )
#                 publish(
#                     mqtt_client,
#                     client + "_control",
#                     json.dumps(
#                         {
#                             "action": "accept",
#                             "message": temp_topic,
#                             "client": (mqtt_client._client_id).decode("utf-8"),
#                         },
#                     ),
#                 )

#         case "accept":
#             client = json["client"]
#             if json["message"] == (mqtt_client._client_id).decode("utf-8"):
#                 temp_topic = (
#                     (mqtt_client._client_id).decode("utf-8") + client + "_timestamp"
#                 )
#                 publish(
#                     mqtt_client,
#                     client + "_control",
#                     json.dumps(
#                         {
#                             "action": "accept",
#                             "message": temp_topic,
#                             "client": (mqtt_client._client_id).decode("utf-8"),
#                         },
#                     ),
#                 )
