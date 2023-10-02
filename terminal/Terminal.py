class Terminal:
    def __init__():
        pass

    @staticmethod
    def main_screen():
        print("O que deseja fazer?")
        print("1 - Listar destinatários possíveis") # Listagem dos usuários e seus respectivos status (online/offline);
        print("2 - Criar grupo") # Criação de grupo (caso o grupo não exista, o criador do grupo se autodeclara líder do mesmo).
        print("3 - Listar grupos cadastrados") # Listagem dos grupos cadastrados: para cada grupo, listar o nome do grupo, líder e demais membros;
        print("4 - Iniciar uma conversa") # Solicitação de conversa e, para depuração, listagem do histórico de solicitação recebidas,
        # bem como listagem das confirmações de aceitação da solicitação de batepapo (listar, apenas para depuração,
        # a informação do tópico criado para iniciar o bate-papo).

    def handle_option(self):
        Terminal.main_screen()

    def list_destinations(self):
        pass

    def create_group(self):
        pass

    def list_registed_groups(self):
        pass

    def start_conversation(self):
        pass