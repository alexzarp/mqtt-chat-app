from functions.connect import connect_mqtt
from functions.publish import publish

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client, "topic", "msg")
    client.loop_stop()


if __name__ == '__main__':
    run()