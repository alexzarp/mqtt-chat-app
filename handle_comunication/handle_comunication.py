from paho.mqtt import client as mqtt_client


def display_message(client, message):
    print(f"Mensagem de {client}: {message}")


def action(mqtt_client: mqtt_client.Client, userdata, msg):
    import json
    import logging

    json = json.loads(msg.payload.decode())
    print(json)
