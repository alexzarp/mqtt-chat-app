from paho.mqtt import client as mqtt_client


def list_destinations(storage="data/storage.json"):
    import json

    print("\nStatus dos usuários conhecidos:")
    with open(storage, "r") as arquivo:
        local = json.load(arquivo)

    for key in local.keys():
        print(f"{key}: {local[key]['status']}")


def list_joined_groups(storage):
    import json

    print("\nGrupos cadastrados:")
    try:
        with open(storage, "r") as arquivo:
            local = json.load(arquivo)
    except:
        print("Nenhum grupo cadastrado.")
        return

    for key in local.keys():
        print(f"Líder {key}: {local[key]['name']}")
