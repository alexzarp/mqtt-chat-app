from functions.connect import connect_mqtt
from functions.publish import publish
from terminal.Terminal import Terminal
from functions.subscribe import subscribe
from functions.online import online
from threading import Thread
from handle_comunication.handle_comunication import *
import json


def run():
    client_mqtt = connect_mqtt()
    online(client_mqtt)

    subscribe(
        client_mqtt=client_mqtt,
        topic="global_control",
        on_message=action,
    )
    print(client_mqtt._client_id)
    subscribe(
        client_mqtt=client_mqtt,
        topic=client_mqtt._client_id.decode("utf-8") + "_control",
        on_message=action,
    )

    terminal = Terminal(client_mqtt=client_mqtt)
    terminal_thread = Thread(target=terminal.main_screen, args=()).start()

    try:
        client_mqtt.loop_start()
    except KeyboardInterrupt:
        print("Exiting...")
        online(client_mqtt=client_mqtt, online=False)
        client_mqtt.loop_stop()

    # terminal_thread.join()


if __name__ == "__main__":
    run()
