import paho.mqtt.client as mqtt_client


def subscribe(client_mqtt: mqtt_client, topic: bytes, on_message: callable):
    # def on_message(client, userdata, msg):
    #     print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    #     return {"topic": msg.topic, "payload": msg.payload.decode()}

    client_mqtt.subscribe(topic)
    client_mqtt.on_message = on_message
