from os import system
from functions.list_destinations import list_destinations

# from functions.create_group import create_group
# from functions.list_registed_groups import list_registed_groups
from functions.start_conversation import start_conversation


class Terminal:
    def __init__(self, client_mqtt):
        self.client_mqtt = client_mqtt
        # self.option = None
        self.type = None

    def main_screen(self):
        # system("clear")
        print("O que deseja fazer?")
        print(
            "1 - Listar destinatários possíveis"
        )  # Listagem dos usuários e seus respectivos status (online/offline);
        print(
            "2 - Criar grupo"
        )  # Criação de grupo (caso o grupo não exista, o criador do grupo se autodeclara líder do mesmo).
        print(
            "3 - Listar grupos cadastrados"
        )  # Listagem dos grupos cadastrados: para cada grupo, listar o nome do grupo, líder e demais membros;
        print("4 - Entrar em um grupo")
        print(
            "5 - Iniciar uma conversa"
        )  # Solicitação de conversa e, para depuração, listagem do histórico de solicitação recebidas,
        # bem como listagem das confirmações de aceitação da solicitação de batepapo (listar, apenas para depuração,
        # a informação do tópico criado para iniciar o bate-papo).
        print("5 - Entrar num grupo")
        match self.handle_option():
            case 1:
                list_destinations(client_mqtt=self.client_mqtt)
            case 2:
                # create_group()
                pass
            case 3:
                # list_registed_groups()
                pass
            case 4:
                print("Para qual destinatário?: ")
                topic = self.handle_option()
                print("Digite a mensagem: \n>>> ")
                message = self.handle_option()
                start_conversation(
                    client_mqtt=self.client_mqtt,
                    topic=topic,
                    message=message,
                )
            case _:
                print("Opção inválida!!")
                self.main_screen()

    def handle_option(self):
        return input()
        # match type:
        #     case isinstance(type, int):
        #         self.type = int()
        #     case isinstance(type, str):
        #         self.type = str()
        #     case _:
        #         print("Tipo inválido!!")
        #         self.handle_option(type=type)

        try:
            option = self.type(input())
        except ValueError:
            print("Opção inválida!!")
            self.main_screen()
        return option
