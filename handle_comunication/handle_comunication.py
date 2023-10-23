def display_message(client, message):
    print("Mensagem de {}: {}".format{client, message})

def action(client, userdata, msg):
    import json
    import logging
    # def on_message(client, userdata, msg):
    #     print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    #     return {"topic": msg.topic, "payload": msg.payload.decode()}
    json = json.loads(msg.payload.decode())
    topic = msg.topic

    for key, value in json.items():
        match key:
            case "action":
                match value:
                    case "conversation":
                        display_message(client, json["message"])
                        logging.info("Mensagem de {}: {}".format{client, json["message"]})
                    case "online":
                        display_message(client, "online")
                    case "offline":
                        display_message(client, "offline")
                    case "status":
                        display_message(client, "status")
                    case "error":
                        display_message(client, "error")
                    case _:
                        display_message(client, "error")
