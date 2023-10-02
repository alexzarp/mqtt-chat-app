from functions.connect import connect_mqtt
from functions.publish import publish
from terminal.Terminal import Terminal
from threading import Thread

def run():
    terminal = Terminal(connect_mqtt())

    terminal_thread = Thread(target=Terminal.main_screen, args=()).start()

    terminal.client_mqtt.loop_start()
    publish(terminal.client_mqtt, "topic", "msg")
    terminal.client_mqtt.loop_stop()

    terminal_thread.join()


if __name__ == '__main__':
    run()