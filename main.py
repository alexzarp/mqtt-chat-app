from functions.connect import connect_mqtt
from functions.publish import publish
from terminal.terminal import Terminal
from functions.subscribe import subscribe
from functions.online import online
from threading import Thread
from handle_comunication.handle_comunication import *
import json
import os
import sys


def run():
    os.system("clear")
    client_mqtt = connect_mqtt()
    online(client_mqtt)

    subscribe(
        client_mqtt=client_mqtt,
        topic="users",
        on_message=monitor,
    )

    subscribe(
        client_mqtt=client_mqtt,
        topic=(client_mqtt._client_id).decode("utf-8") + "_control",
        on_message=mytopic,
    )

    subscribe(
        client_mqtt=client_mqtt,
        topic="groups",
        on_message=groups_handle,
    )

    susbscribe_lasts(client_mqtt)

    try:
        client_mqtt.loop_start()
        terminal = Terminal(client_mqtt=client_mqtt)
        terminal.main_screen()
    except (KeyboardInterrupt, EOFError):
        print("Exiting...")
        online(client_mqtt=client_mqtt, online=False)
        client_mqtt.loop_stop()

    # terminal_thread.join()


if __name__ == "__main__":
    run()
