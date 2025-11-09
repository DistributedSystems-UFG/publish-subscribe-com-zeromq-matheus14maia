import zmq
import time
import threading
from constPS import *

class ChatPublisher:
    """
    Publisher para sistema de chat em grupo baseado em tópicos.
    Cada grupo/tópico representa uma sala de chat diferente.
    """
    
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.address = f"tcp://{HOST}:{PORT}"
        self.socket.bind(self.address)
        
        # Lista de tópicos/grupos disponíveis
        self.topics = [
            "GERAL",
            "TECNOLOGIA", 
            "ESPORTES",
            "ENTRETENIMENTO",
            "NOTICIAS",
            "SISTEMA"
        ]
        
        print("=" * 60)
        print("SERVIDOR PUBLISHER - SISTEMA DE CHAT POR TÓPICOS")
        print("=" * 60)
        print(f"Servidor iniciado em {self.address}")
        print(f"\nTópicos/Grupos disponíveis: {', '.join(self.topics)}")
        print("=" * 60)
        
        # Enviar mensagem de boas-vindas
        time.sleep(1)  # Aguardar para conexões iniciais
        self.send_system_message("Servidor de chat iniciado!")
    
    def send_message(self, topic, username, message):
        """Envia uma mensagem para um tópico específico"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_msg = f"{topic} [{timestamp}] {username}: {message}"
        self.socket.send_string(formatted_msg)
        print(f"Enviado -> {formatted_msg}")
    
    def send_system_message(self, message):
        """Envia uma mensagem do sistema para o tópico SISTEMA"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_msg = f"SISTEMA [{timestamp}] [SISTEMA]: {message}"
        self.socket.send_string(formatted_msg)
        print(f"Sistema -> {formatted_msg}")
    
    def broadcast_to_all(self, username, message):
        """Envia uma mensagem para todos os tópicos"""
        for topic in self.topics:
            if topic != "SISTEMA":
                self.send_message(topic, username, message)
    
    def run_interactive_mode(self):
        """Modo interativo para o publisher enviar mensagens"""
        print("\n" + "=" * 60)
        print("MODO INTERATIVO DO PUBLISHER")
        print("=" * 60)
        print("Comandos disponíveis:")
        print("  - Digite o número do tópico + mensagem")
        print("  - Formato: <número_tópico> <nome_usuario> <mensagem>")
        print("  - Exemplo: 1 Admin Olá a todos!")
        print("  - Digite 'broadcast <usuario> <msg>' para enviar a todos")
        print("  - Digite 'sair' para encerrar")
        print("=" * 60)
        
        # Exibir tópicos numerados
        print("\nTópicos disponíveis:")
        for i, topic in enumerate(self.topics, 1):
            if topic != "SISTEMA":
                print(f"  {i}. {topic}")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if user_input.lower() == 'sair':
                    self.send_system_message("Servidor sendo encerrado...")
                    print("Encerrando servidor...")
                    break
                
                if user_input.startswith('broadcast '):
                    parts = user_input.split(' ', 2)
                    if len(parts) >= 3:
                        username = parts[1]
                        message = parts[2]
                        self.broadcast_to_all(username, message)
                    else:
                        print("Formato inválido. Use: broadcast <usuario> <mensagem>")
                    continue
                
                # Processar mensagem para tópico específico
                parts = user_input.split(' ', 2)
                if len(parts) >= 3:
                    try:
                        topic_num = int(parts[0])
                        if 1 <= topic_num <= len(self.topics) and self.topics[topic_num-1] != "SISTEMA":
                            topic = self.topics[topic_num - 1]
                            username = parts[1]
                            message = parts[2]
                            self.send_message(topic, username, message)
                        else:
                            print(f"Número de tópico inválido. Use 1-{len(self.topics)-1}")
                    except ValueError:
                        print("Formato inválido. Use: <número_tópico> <usuario> <mensagem>")
                else:
                    print("Formato inválido. Use: <número_tópico> <usuario> <mensagem>")
                    
            except KeyboardInterrupt:
                print("\n\nEncerrando servidor...")
                self.send_system_message("Servidor encerrado por interrupção")
                break
            except Exception as e:
                print(f"Erro: {e}")
    
    def run_automatic_mode(self):
        """Modo automático que envia mensagens periodicamente"""
        print("\nModo automático ativado - enviando mensagens periódicas...")
        print("Pressione Ctrl+C para parar\n")
        
        counter = 0
        try:
            while True:
                time.sleep(10)
                counter += 1
                
                # Alternar entre diferentes tópicos
                topic_index = counter % (len(self.topics) - 1)
                topic = self.topics[topic_index]
                
                if topic == "SISTEMA":
                    continue
                
                # Mensagens automáticas variadas
                messages = [
                    "Bem-vindos ao chat!",
                    "Alguém online?",
                    "Sistema funcionando normalmente",
                    "Nova atualização disponível",
                    "Chat ativo!"
                ]
                
                message = messages[counter % len(messages)]
                self.send_message(topic, "Bot", message)
                
        except KeyboardInterrupt:
            print("\n\nModo automático interrompido")
            self.send_system_message("Modo automático encerrado")

def main():
    publisher = ChatPublisher()
    
    print("\nEscolha o modo de operação:")
    print("1. Modo Interativo (enviar mensagens manualmente)")
    print("2. Modo Automático (enviar mensagens automáticas)")
    
    choice = input("\nOpção (1 ou 2): ").strip()
    
    if choice == "1":
        publisher.run_interactive_mode()
    elif choice == "2":
        publisher.run_automatic_mode()
    else:
        print("Opção inválida. Iniciando modo interativo...")
        publisher.run_interactive_mode()

if __name__ == "__main__":
    main()
