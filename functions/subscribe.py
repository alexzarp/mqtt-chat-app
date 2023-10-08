import paho.mqtt.client as mqtt_client

def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        return {
            "topic": msg.topic,
            "payload": msg.payload.decode()
        }

    client.subscribe(topic)
    client.on_message = on_message
