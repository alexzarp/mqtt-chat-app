from time import sleep
from paho.mqtt import client as mqtt_client


def publish(mqtt_client: mqtt_client.Client, topic, payload):
    while True:
        sleep(1)
        result = mqtt_client.publish(topic, payload)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"\nEnviando `{payload}` ao tópico `{topic}`\n")
            break
        else:
            print(f"Failed to send message to topic {topic}")
