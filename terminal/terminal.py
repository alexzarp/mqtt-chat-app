from os import system
from functions.list_destinations import list_destinations
from paho.mqtt import client as mqtt_client
from functions.online import online
from functions.create_group import create_group
from functions.subscribe import unsubscribe

# from functions.list_registed_groups import list_registed_groups
from functions.start_conversation import *
import queue


class Terminal:
    def __init__(self, client_mqtt: mqtt_client.Client):
        self.client_mqtt = client_mqtt

    def main_screen(self):
        while 1:
            txt = "\n"
            txt += "O que deseja fazer?\n"
            txt += "1 - Listar destinatários possíveis\n"  # Listagem dos usuários e seus respectivos status (online/offline);
            txt += "2 - Iniciar uma conversa\n"  # Solicitação de conversa e, para depuração, listagem do histórico de solicitação recebidas,
            txt += "3 - Enviar mensagem\n"
            txt += "4 - Criar grupo\n"  # Criação de grupo (caso o grupo não exista, o criador do grupo se autodeclara líder do mesmo).
            txt += "5 - Entrar em um grupo\n"
            txt += "6 - Listar grupos cadastrados\n"  # Listagem dos grupos cadastrados: para cada grupo, listar o nome do grupo, líder e demais membros;
            # bem como listagem das confirmações de aceitação da solicitação de batepapo (listar, apenas para depuração,
            # a informação do tópico criado para iniciar o bate-papo).
            txt += "7 - Fechar uma conversa\n"
            txt += "8 - Sair do sistema\n"
            print(txt)

            match self.handle_option(time=0.2):
                case 1:
                    list_destinations()
                case 2:
                    topic = input("Para qual destinatáio: ")
                    # message = input("Digite a mensagem: \n>>> ")
                    start_conversation(
                        client_mqtt=self.client_mqtt,
                        topic=topic,
                    )
                case 3:
                    send_message(client_mqtt=self.client_mqtt)
                case 4:
                    create_group()
                    pass
                case 5:
                    pass
                case 6:
                    topic = input("Qual conversa deseja fechar: \n>>>")
                    try:
                        unsubscribe(client_mqtt=mqtt_client, topic=topic)
                        print(f"Conversa {topic} fechada.")
                    except:
                        print(f"Não foi possível fechar a conversa {topic}.")
                case 7:
                    print("Exiting...")
                    online(client_mqtt=self.client_mqtt, online=False)
                    self.client_mqtt.loop_stop()
                    exit(1)
                case _:
                    print("Opção inválida!!")
                    self.main_screen()

    def handle_option(self, time: float = None):
        from time import sleep
        import re

        padrao = re.compile(r"^\d")
        if time:
            sleep(time)
        while True:
            op = input()
            if bool(padrao.match(op)):
                return int(op)
            else:
                continue
