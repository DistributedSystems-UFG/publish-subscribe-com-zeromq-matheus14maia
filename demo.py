"""
Script de demonstração do sistema de chat Publish-Subscribe
Este script simula múltiplos usuários interagindo em diferentes tópicos
"""

import zmq
import time
import threading
from constPS import *

class ChatDemo:
    """Demonstração automatizada do sistema de chat"""
    
    def __init__(self):
        # Configurar publisher
        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind(f"tcp://{HOST}:{PORT}")
        
        # Lista de tópicos
        self.topics = ["GERAL", "TECNOLOGIA", "ESPORTES", "ENTRETENIMENTO", "NOTICIAS", "SISTEMA"]
        
        print("=" * 70)
        print("DEMONSTRAÇÃO DO SISTEMA DE CHAT PUBLISH-SUBSCRIBE")
        print("=" * 70)
        print(f"Servidor iniciado em tcp://{HOST}:{PORT}")
        print(f"Tópicos disponíveis: {', '.join(self.topics)}")
        print("=" * 70)
        
        time.sleep(1)  # Aguardar conexões iniciais
    
    def create_subscriber(self, username, topics_to_subscribe):
        """Cria um subscriber e inicia thread de recebimento"""
        sub_socket = self.context.socket(zmq.SUB)
        sub_socket.connect(f"tcp://{HOST}:{PORT}")
        
        # Inscrever nos tópicos
        for topic in topics_to_subscribe:
            sub_socket.setsockopt_string(zmq.SUBSCRIBE, topic)
        
        def receive_messages():
            print(f"\n[{username}] Conectado! Inscrito em: {', '.join(topics_to_subscribe)}")
            while True:
                try:
                    if sub_socket.poll(100):
                        message = sub_socket.recv_string()
                        print(f"[{username}] 📩 {message}")
                except:
                    break
        
        thread = threading.Thread(target=receive_messages, daemon=True)
        thread.start()
        return sub_socket
    
    def send_message(self, topic, username, message):
        """Envia uma mensagem para um tópico"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_msg = f"{topic} [{timestamp}] {username}: {message}"
        self.pub_socket.send_string(formatted_msg)
        print(f"\n📤 Enviado: {formatted_msg}")
    
    def run_demo(self):
        """Executa a demonstração"""
        print("\n🎬 Iniciando demonstração em 2 segundos...\n")
        time.sleep(2)
        
        # Criar subscribers com diferentes interesses
        print("\n" + "=" * 70)
        print("CRIANDO USUÁRIOS...")
        print("=" * 70)
        
        # João gosta de tecnologia e notícias
        joao = self.create_subscriber("João", ["TECNOLOGIA", "NOTICIAS", "SISTEMA"])
        time.sleep(0.5)
        
        # Maria gosta de esportes e entretenimento
        maria = self.create_subscriber("Maria", ["ESPORTES", "ENTRETENIMENTO", "SISTEMA"])
        time.sleep(0.5)
        
        # Pedro está inscrito em tudo
        pedro = self.create_subscriber("Pedro", self.topics)
        time.sleep(0.5)
        
        # Ana só quer chat geral
        ana = self.create_subscriber("Ana", ["GERAL", "SISTEMA"])
        time.sleep(1)
        
        print("\n" + "=" * 70)
        print("SIMULANDO CONVERSAS...")
        print("=" * 70)
        
        # Cenário 1: Mensagem no chat geral
        time.sleep(2)
        print("\n--- Cenário 1: Chat Geral ---")
        self.send_message("GERAL", "Admin", "Bem-vindos ao sistema de chat!")
        time.sleep(2)
        
        # Cenário 2: Discussão sobre tecnologia
        print("\n--- Cenário 2: Tópico Tecnologia ---")
        self.send_message("TECNOLOGIA", "TechGuru", "Python 3.12 foi lançado!")
        time.sleep(1)
        self.send_message("TECNOLOGIA", "DevMaster", "Que novidades interessantes!")
        time.sleep(2)
        
        # Cenário 3: Notícias de esportes
        print("\n--- Cenário 3: Tópico Esportes ---")
        self.send_message("ESPORTES", "SportsFan", "Grande jogo hoje à noite!")
        time.sleep(1)
        self.send_message("ESPORTES", "CoachPro", "Time está em ótima forma!")
        time.sleep(2)
        
        # Cenário 4: Entretenimento
        print("\n--- Cenário 4: Tópico Entretenimento ---")
        self.send_message("ENTRETENIMENTO", "CineLover", "Novo filme estreou hoje!")
        time.sleep(1)
        self.send_message("ENTRETENIMENTO", "MusicFan", "Show imperdível no fim de semana!")
        time.sleep(2)
        
        # Cenário 5: Notícias importantes
        print("\n--- Cenário 5: Tópico Notícias ---")
        self.send_message("NOTICIAS", "Reporter", "Importante atualização econômica")
        time.sleep(2)
        
        # Cenário 6: Mensagem do sistema
        print("\n--- Cenário 6: Mensagem do Sistema ---")
        self.send_message("SISTEMA", "SISTEMA", "Servidor funcionando perfeitamente!")
        time.sleep(2)
        
        # Cenário 7: Múltiplas mensagens simultâneas
        print("\n--- Cenário 7: Múltiplos Tópicos Simultaneamente ---")
        self.send_message("GERAL", "User1", "Alguém online?")
        self.send_message("TECNOLOGIA", "User2", "Discutindo IA...")
        self.send_message("ESPORTES", "User3", "Resultado do jogo!")
        time.sleep(3)
        
        print("\n" + "=" * 70)
        print("DEMONSTRAÇÃO CONCLUÍDA")
        print("=" * 70)
        print("\n📊 Resumo:")
        print("  • João recebeu mensagens de: TECNOLOGIA, NOTICIAS, SISTEMA")
        print("  • Maria recebeu mensagens de: ESPORTES, ENTRETENIMENTO, SISTEMA")
        print("  • Pedro recebeu TODAS as mensagens (inscrito em todos os tópicos)")
        print("  • Ana recebeu mensagens de: GERAL, SISTEMA")
        print("\n💡 Cada usuário recebeu apenas as mensagens dos tópicos de seu interesse!")
        print("=" * 70)
        
        time.sleep(2)
        print("\n✅ Demo finalizada. Pressione Ctrl+C para sair.")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n👋 Encerrando demonstração...")

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║          DEMO: Sistema de Chat Publish-Subscribe                ║
    ║                     com ZeroMQ                                   ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    Esta demonstração mostrará:
    ✓ Múltiplos usuários com interesses diferentes
    ✓ Mensagens em diversos tópicos
    ✓ Filtro automático de mensagens por tópico
    ✓ Comunicação assíncrona publish-subscribe
    
    """)
    
    input("Pressione ENTER para iniciar a demonstração...")
    
    demo = ChatDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()

