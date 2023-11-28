import paho.mqtt.client as mqtt_client


def subscribe(client_mqtt: mqtt_client.Client, topic: bytes, on_message: callable):
    # def on_message(client, userdata, msg):
    #     print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    #     return {"topic": msg.topic, "payload": msg.payload.decode()}

    client_mqtt.subscribe(topic)
    client_mqtt.message_callback_add(topic, on_message)


# self.client.subscribe("GROUPS/#", 2)
# self.client.subscribe("USERS/#", 2)
# self.client.subscribe(f"{self.id}_CONTROL", 2)

# # assinaturas personalizadas
# self.client.message_callback_add(f"{self.id}_CONTROL", onControlMessage)
# self.client.message_callback_add("USERS/#", onUserStatusMessage)
# self.client.message_callback_add("GROUPS/#", onGroupListMessage)
