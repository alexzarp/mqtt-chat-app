from paho.mqtt import client as mqtt_client


def list_destinations(storage="data/storage.json"):
    import json

    print("\nStatus dos usuários conhecidos:")
    with open(storage, "r") as arquivo:
        local = json.load(arquivo)

    for key in local.keys():
        print(f"{key}: {local[key]['status']}")
