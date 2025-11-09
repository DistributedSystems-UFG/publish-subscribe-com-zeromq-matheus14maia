import zmq
import threading
import time
from constPS import *

class ChatSubscriber:
    """
    Subscriber para sistema de chat em grupo baseado em tópicos.
    Permite inscrição em múltiplos tópicos/grupos simultaneamente.
    """
    
    def __init__(self, username):
        self.username = username
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.address = f"tcp://{HOST}:{PORT}"
        self.socket.connect(self.address)
        
        # Lista de tópicos disponíveis
        self.available_topics = [
            "GERAL",
            "TECNOLOGIA", 
            "ESPORTES",
            "ENTRETENIMENTO",
            "NOTICIAS",
            "SISTEMA"
        ]
        
        self.subscribed_topics = []
        self.running = False
        
        print("=" * 60)
        print(f"CHAT CLIENT - Usuário: {self.username}")
        print("=" * 60)
        print(f"Conectado ao servidor em {self.address}")
        print("=" * 60)
    
    def subscribe_to_topic(self, topic):
        """Inscreve-se em um tópico específico"""
        if topic not in self.subscribed_topics:
            self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)
            self.subscribed_topics.append(topic)
            print(f"✓ Inscrito no tópico: {topic}")
            return True
        else:
            print(f"✗ Já inscrito no tópico: {topic}")
            return False
    
    def unsubscribe_from_topic(self, topic):
        """Cancela inscrição de um tópico"""
        if topic in self.subscribed_topics:
            self.socket.setsockopt_string(zmq.UNSUBSCRIBE, topic)
            self.subscribed_topics.remove(topic)
            print(f"✓ Desinscrição do tópico: {topic}")
            return True
        else:
            print(f"✗ Não está inscrito no tópico: {topic}")
            return False
    
    def subscribe_to_all(self):
        """Inscreve-se em todos os tópicos disponíveis"""
        for topic in self.available_topics:
            self.subscribe_to_topic(topic)
    
    def list_topics(self):
        """Lista todos os tópicos disponíveis"""
        print("\nTópicos disponíveis:")
        for i, topic in enumerate(self.available_topics, 1):
            status = "✓" if topic in self.subscribed_topics else " "
            print(f"  [{status}] {i}. {topic}")
    
    def receive_messages(self):
        """Thread para receber mensagens continuamente"""
        self.running = True
        print("\n" + "=" * 60)
        print("RECEBENDO MENSAGENS (Ctrl+C para comandos)")
        print("=" * 60 + "\n")
        
        while self.running:
            try:
                # Usar polling para verificar se há mensagens
                if self.socket.poll(100):  # 100ms timeout
                    message = self.socket.recv_string()
                    
                    # Colorir output baseado no tópico
                    if message.startswith("SISTEMA"):
                        print(f"\n🔔 {message}")
                    else:
                        print(f"\n💬 {message}")
                        
            except zmq.ZMQError as e:
                if self.running:
                    print(f"Erro ao receber mensagem: {e}")
            except Exception as e:
                if self.running:
                    print(f"Erro inesperado: {e}")
    
    def show_menu(self):
        """Exibe o menu de comandos"""
        print("\n" + "=" * 60)
        print("COMANDOS DISPONÍVEIS")
        print("=" * 60)
        print("  1. listar         - Listar tópicos disponíveis")
        print("  2. inscrever      - Inscrever em um tópico")
        print("  3. desinscrever   - Desinscrever de um tópico")
        print("  4. todos          - Inscrever em todos os tópicos")
        print("  5. inscritos      - Ver tópicos inscritos")
        print("  6. ajuda          - Mostrar este menu")
        print("  7. sair           - Sair do chat")
        print("=" * 60)
    
    def run_interactive(self):
        """Executa o subscriber em modo interativo"""
        # Sempre se inscrever em SISTEMA para receber notificações
        self.subscribe_to_topic("SISTEMA")
        
        # Iniciar thread de recebimento de mensagens
        receiver_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receiver_thread.start()
        
        self.show_menu()
        
        print("\n💡 Dica: Inscreva-se em pelo menos um tópico para receber mensagens!")
        print("Digite 'ajuda' para ver os comandos disponíveis.\n")
        
        while True:
            try:
                command = input("\nComando > ").strip().lower()
                
                if command == 'sair':
                    print("\nEncerrando chat...")
                    self.running = False
                    time.sleep(0.5)
                    break
                
                elif command == 'listar':
                    self.list_topics()
                
                elif command == 'inscrever':
                    self.list_topics()
                    topic_num = input("\nNúmero do tópico: ").strip()
                    try:
                        idx = int(topic_num) - 1
                        if 0 <= idx < len(self.available_topics):
                            self.subscribe_to_topic(self.available_topics[idx])
                        else:
                            print("Número inválido!")
                    except ValueError:
                        print("Digite um número válido!")
                
                elif command == 'desinscrever':
                    if not self.subscribed_topics:
                        print("Você não está inscrito em nenhum tópico!")
                        continue
                    
                    print("\nTópicos inscritos:")
                    for i, topic in enumerate(self.subscribed_topics, 1):
                        if topic != "SISTEMA":  # Não permitir desinscrever de SISTEMA
                            print(f"  {i}. {topic}")
                    
                    topic_num = input("\nNúmero do tópico para desinscrever: ").strip()
                    try:
                        idx = int(topic_num) - 1
                        if 0 <= idx < len(self.subscribed_topics):
                            topic = self.subscribed_topics[idx]
                            if topic != "SISTEMA":
                                self.unsubscribe_from_topic(topic)
                            else:
                                print("Não é possível desinscrever do tópico SISTEMA!")
                        else:
                            print("Número inválido!")
                    except ValueError:
                        print("Digite um número válido!")
                
                elif command == 'todos':
                    self.subscribe_to_all()
                
                elif command == 'inscritos':
                    if self.subscribed_topics:
                        print("\nTópicos inscritos:")
                        for topic in self.subscribed_topics:
                            print(f"  ✓ {topic}")
                    else:
                        print("\nVocê não está inscrito em nenhum tópico!")
                
                elif command == 'ajuda':
                    self.show_menu()
                
                elif command == '':
                    continue
                
                else:
                    print(f"Comando desconhecido: '{command}'")
                    print("Digite 'ajuda' para ver os comandos disponíveis.")
                    
            except KeyboardInterrupt:
                print("\n\nEncerrando chat...")
                self.running = False
                time.sleep(0.5)
                break
            except Exception as e:
                print(f"Erro: {e}")
    
    def run_simple(self, topics=None, duration=None):
        """
        Modo simples: inscreve em tópicos específicos e recebe mensagens
        
        Args:
            topics: Lista de tópicos para se inscrever (None = todos)
            duration: Duração em segundos (None = indefinido)
        """
        # Inscrever em tópicos
        if topics is None:
            self.subscribe_to_all()
        else:
            for topic in topics:
                if topic in self.available_topics:
                    self.subscribe_to_topic(topic)
        
        print("\n" + "=" * 60)
        print("RECEBENDO MENSAGENS")
        print("=" * 60)
        print("Pressione Ctrl+C para parar\n")
        
        start_time = time.time()
        try:
            while True:
                message = self.socket.recv_string()
                print(f"📩 {message}")
                
                # Verificar duração
                if duration and (time.time() - start_time) >= duration:
                    print(f"\n⏰ Tempo de {duration} segundos esgotado.")
                    break
                    
        except KeyboardInterrupt:
            print("\n\n✋ Chat interrompido pelo usuário")

def main():
    print("=" * 60)
    print("BEM-VINDO AO SISTEMA DE CHAT POR TÓPICOS")
    print("=" * 60)
    
    username = input("\nDigite seu nome de usuário: ").strip()
    if not username:
        username = "Anônimo"
    
    subscriber = ChatSubscriber(username)
    
    print("\nEscolha o modo de operação:")
    print("1. Modo Interativo (gerenciar inscrições)")
    print("2. Modo Simples (receber mensagens de todos os tópicos)")
    print("3. Modo Personalizado (escolher tópicos iniciais)")
    
    choice = input("\nOpção (1, 2 ou 3): ").strip()
    
    if choice == "1":
        subscriber.run_interactive()
    elif choice == "2":
        subscriber.run_simple()
    elif choice == "3":
        subscriber.list_topics()
        topic_nums = input("\nDigite os números dos tópicos (separados por vírgula): ").strip()
        try:
            indices = [int(x.strip()) - 1 for x in topic_nums.split(',')]
            topics = [subscriber.available_topics[i] for i in indices if 0 <= i < len(subscriber.available_topics)]
            subscriber.run_simple(topics=topics)
        except:
            print("Entrada inválida. Inscrevendo em todos os tópicos...")
            subscriber.run_simple()
    else:
        print("Opção inválida. Iniciando modo interativo...")
        subscriber.run_interactive()

if __name__ == "__main__":
    main()
