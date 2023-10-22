from functions.connect import connect_mqtt
from functions.publish import publish
from terminal.Terminal import Terminal
from functions.subscribe import subscribe
from functions.online import online
from threading import Thread


def run():
    client_mqtt = connect_mqtt()
    subscribe(client_mqtt=client_mqtt, topic="global_control")
    subscribe(client_mqtt=client_mqtt, topic=client_mqtt._client_id + "_control")

    Thread(target=online, args=(client_mqtt)).start()

    terminal = Terminal(client_mqtt=client_mqtt)
    terminal_thread = Thread(target=terminal.main_screen, args=()).start()

    try:
        client_mqtt.loop_start()
    except KeyboardInterrupt:
        print("Exiting...")
        client_mqtt.loop_stop()

    terminal_thread.join()


if __name__ == "__main__":
    run()
