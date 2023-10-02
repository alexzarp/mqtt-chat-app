from functions.connect import connect_mqtt
from functions.publish import publish
from terminal.Terminal import Terminal
from threading import Thread

def run():
    terminal = Thread(target=Terminal.main_screen, args=()).start()
    client = connect_mqtt()
    client.loop_start()
    publish(client, "topic", "msg")
    client.loop_stop()
    terminal.join()


if __name__ == '__main__':
    run()