"""
Exemplo de extensão do sistema de chat com tópicos personalizados
Demonstra como adicionar novos tópicos e funcionalidades
"""

import zmq
import time
import json
from constPS import *

class ChatExtendido:
    """
    Exemplo de como estender o sistema de chat com funcionalidades extras:
    - Tópicos personalizados
    - Mensagens com metadados (JSON)
    - Prioridades de mensagens
    - Mensagens privadas usando tópicos únicos
    """
    
    def __init__(self):
        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind(f"tcp://{HOST}:{PORT}")
        
        # Tópicos personalizados para diferentes disciplinas
        self.topics = {
            "SD": "Sistemas Distribuídos",
            "BD": "Banco de Dados",
            "RC": "Redes de Computadores",
            "IA": "Inteligência Artificial",
            "ES": "Engenharia de Software",
            "AVISOS": "Avisos Gerais",
            "DUVIDAS": "Dúvidas",
            "PROJETOS": "Discussão de Projetos"
        }
        
        print("=" * 70)
        print("SISTEMA DE CHAT ESTENDIDO - Ambiente Acadêmico")
        print("=" * 70)
        print("\nTópicos disponíveis:")
        for code, name in self.topics.items():
            print(f"  • {code}: {name}")
        print("=" * 70)
        
        time.sleep(1)
    
    def send_simple_message(self, topic, username, message):
        """Envia mensagem simples (formato original)"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_msg = f"{topic} [{timestamp}] {username}: {message}"
        self.pub_socket.send_string(formatted_msg)
        print(f"✓ Enviado para {topic}: {message}")
    
    def send_structured_message(self, topic, username, message, metadata=None):
        """
        Envia mensagem estruturada com metadados em JSON
        Útil para mensagens com prioridade, anexos, etc.
        """
        msg_data = {
            "topic": topic,
            "username": username,
            "message": message,
            "timestamp": time.time(),
            "formatted_time": time.strftime("%H:%M:%S"),
            "metadata": metadata or {}
        }
        
        # O tópico ainda é enviado como prefixo para o filtro do ZeroMQ
        formatted_msg = f"{topic} {json.dumps(msg_data, ensure_ascii=False)}"
        self.pub_socket.send_string(formatted_msg)
        print(f"✓ Enviado (estruturado) para {topic}")
    
    def send_priority_message(self, topic, username, message, priority="normal"):
        """Envia mensagem com prioridade"""
        self.send_structured_message(
            topic, 
            username, 
            message,
            metadata={"priority": priority}
        )
    
    def send_file_notification(self, topic, username, filename, file_url):
        """Envia notificação de arquivo compartilhado"""
        message = f"Compartilhou: {filename}"
        self.send_structured_message(
            topic,
            username,
            message,
            metadata={
                "type": "file",
                "filename": filename,
                "url": file_url
            }
        )
    
    def send_poll(self, topic, username, question, options):
        """Envia uma enquete para o grupo"""
        message = f"ENQUETE: {question}"
        self.send_structured_message(
            topic,
            username,
            message,
            metadata={
                "type": "poll",
                "question": question,
                "options": options
            }
        )
    
    def demo_basico(self):
        """Demonstração básica com mensagens simples"""
        print("\n--- Demo 1: Mensagens Simples ---\n")
        
        self.send_simple_message("SD", "Professor", "Aula de ZeroMQ hoje às 14h")
        time.sleep(1)
        
        self.send_simple_message("SD", "Aluno1", "Onde será a aula?")
        time.sleep(1)
        
        self.send_simple_message("SD", "Professor", "Laboratório 3")
        time.sleep(2)
    
    def demo_estruturado(self):
        """Demonstração com mensagens estruturadas"""
        print("\n--- Demo 2: Mensagens Estruturadas ---\n")
        
        # Mensagem prioritária
        self.send_priority_message(
            "AVISOS", 
            "Coordenador",
            "URGENTE: Prazo de matrícula termina amanhã!",
            priority="high"
        )
        time.sleep(1)
        
        # Compartilhamento de arquivo
        self.send_file_notification(
            "SD",
            "Professor",
            "Slides_ZeroMQ.pdf",
            "https://exemplo.com/slides.pdf"
        )
        time.sleep(1)
        
        # Enquete
        self.send_poll(
            "PROJETOS",
            "Monitor",
            "Qual o melhor dia para reunião?",
            ["Segunda", "Quarta", "Sexta"]
        )
        time.sleep(2)
    
    def demo_multitopicos(self):
        """Demonstração com múltiplos tópicos"""
        print("\n--- Demo 3: Múltiplos Tópicos Simultaneamente ---\n")
        
        # Diferentes disciplinas ao mesmo tempo
        self.send_simple_message("SD", "Prof_SD", "Trabalho sobre pub-sub devido sexta")
        self.send_simple_message("BD", "Prof_BD", "Prova de SQL na próxima semana")
        self.send_simple_message("IA", "Prof_IA", "Novo material sobre redes neurais")
        time.sleep(1)
        
        # Dúvidas em diferentes tópicos
        self.send_simple_message("DUVIDAS", "Aluno1", "[SD] Como funciona o SUBSCRIBE?")
        self.send_simple_message("DUVIDAS", "Aluno2", "[BD] Diferença entre INNER e LEFT JOIN?")
        time.sleep(2)
    
    def demo_grupo_estudo(self):
        """Simula grupo de estudo"""
        print("\n--- Demo 4: Grupo de Estudo Colaborativo ---\n")
        
        self.send_simple_message("PROJETOS", "Alice", "Vamos dividir as tarefas do projeto?")
        time.sleep(1)
        
        self.send_simple_message("PROJETOS", "Bob", "Eu posso fazer o publisher")
        time.sleep(1)
        
        self.send_simple_message("PROJETOS", "Carol", "Eu faço o subscriber")
        time.sleep(1)
        
        self.send_simple_message("PROJETOS", "Alice", "Ótimo! Eu faço a documentação")
        time.sleep(1)
        
        self.send_file_notification(
            "PROJETOS",
            "Alice",
            "Divisao_Tarefas.docx",
            "https://exemplo.com/tarefas.docx"
        )
        time.sleep(2)

def criar_subscriber_exemplo(username, topics):
    """Cria um subscriber de exemplo que mostra mensagens estruturadas"""
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{HOST}:{PORT}")
    
    for topic in topics:
        socket.setsockopt_string(zmq.SUBSCRIBE, topic)
    
    print(f"\n[{username}] Conectado aos tópicos: {', '.join(topics)}")
    
    while True:
        try:
            message = socket.recv_string()
            
            # Tentar parsear como JSON
            parts = message.split(' ', 1)
            if len(parts) == 2:
                topic = parts[0]
                try:
                    data = json.loads(parts[1])
                    
                    # Exibir com formatação especial baseada no tipo
                    print(f"\n[{username}] 📨 De: {data['username']} ({topic})")
                    print(f"    💬 {data['message']}")
                    
                    if data.get('metadata'):
                        meta = data['metadata']
                        
                        if meta.get('priority') == 'high':
                            print("    ⚠️  ALTA PRIORIDADE")
                        
                        if meta.get('type') == 'file':
                            print(f"    📎 Arquivo: {meta['filename']}")
                            print(f"    🔗 Link: {meta['url']}")
                        
                        if meta.get('type') == 'poll':
                            print(f"    📊 Opções: {', '.join(meta['options'])}")
                    
                except json.JSONDecodeError:
                    # Mensagem simples (não JSON)
                    print(f"\n[{username}] 💬 {message}")
            else:
                print(f"\n[{username}] 💬 {message}")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Erro: {e}")
            break

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║        EXEMPLO DE EXTENSÃO DO SISTEMA DE CHAT                    ║
    ║              Ambiente Acadêmico Colaborativo                     ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    Este exemplo demonstra como estender o sistema básico com:
    
    ✓ Tópicos personalizados (disciplinas)
    ✓ Mensagens estruturadas (JSON)
    ✓ Prioridades de mensagens
    ✓ Compartilhamento de arquivos
    ✓ Enquetes/votações
    ✓ Grupos de estudo colaborativos
    
    """)
    
    print("Escolha uma opção:")
    print("1. Executar todas as demonstrações")
    print("2. Demo básica (mensagens simples)")
    print("3. Demo estruturada (JSON, prioridades, arquivos)")
    print("4. Demo multi-tópicos")
    print("5. Demo grupo de estudo")
    
    choice = input("\nOpção (1-5): ").strip()
    
    chat = ChatExtendido()
    time.sleep(1)
    
    if choice == "1":
        chat.demo_basico()
        chat.demo_estruturado()
        chat.demo_multitopicos()
        chat.demo_grupo_estudo()
    elif choice == "2":
        chat.demo_basico()
    elif choice == "3":
        chat.demo_estruturado()
    elif choice == "4":
        chat.demo_multitopicos()
    elif choice == "5":
        chat.demo_grupo_estudo()
    else:
        print("Opção inválida!")
        return
    
    print("\n" + "=" * 70)
    print("DEMONSTRAÇÃO CONCLUÍDA")
    print("=" * 70)
    print("\n💡 Dica: Você pode criar seu próprio subscriber usando a função")
    print("   'criar_subscriber_exemplo()' para receber estas mensagens!")
    print("\n✨ Este é apenas um exemplo - as possibilidades são infinitas!")
    print("=" * 70)

if __name__ == "__main__":
    main()

