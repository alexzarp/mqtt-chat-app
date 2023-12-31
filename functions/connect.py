from paho.mqtt import client as mqtt_client
import random
import logging
from time import sleep
import sys


def client_id() -> mqtt_client.Client:
    return f"user-{random.randint(0, 99999)}"


def connect_mqtt(broker: str = "localhost", port: int = 1883, id=sys.argv[1]):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(
                f"Connected to MQTT Broker!\n\
Client: {(client._client_id).decode('utf-8')}\n\
User data: {userdata}\n\
Flags: {flags}\n"
            )
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(f"{id}")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(broker, port)
    return client


FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60


def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        sleep(reconnect_delay)

        try:
            client.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
