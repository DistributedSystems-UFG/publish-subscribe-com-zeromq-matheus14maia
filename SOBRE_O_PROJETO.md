# 📝 Sobre o Projeto - Sistema de Chat Publish-Subscribe

## 🎯 Objetivo

Este projeto implementa um **sistema de chat em grupo** utilizando o padrão arquitetural **Publish-Subscribe** com a biblioteca **ZeroMQ**, conforme solicitado na atividade da disciplina de Sistemas Distribuídos.

## ✅ Requisitos Atendidos

### ✔️ Baseado no exemplo do livro (Fig. 4.22)
- Mantidos os arquivos originais `publisher.py` e `subscriber.py`
- Estrutura básica preservada

### ✔️ Novas funcionalidades adicionadas

#### 1. **Múltiplos Tópicos/Grupos**
   - GERAL
   - TECNOLOGIA
   - ESPORTES
   - ENTRETENIMENTO
   - NOTICIAS
   - SISTEMA

#### 2. **Publisher Completo** (`publisher.py`)
   - Modo interativo para enviar mensagens manualmente
   - Modo automático para testes
   - Suporte a broadcast (enviar para todos os tópicos)
   - Mensagens com timestamp
   - Interface amigável com menus

#### 3. **Subscriber Completo** (`subscriber.py`)
   - Inscrição/desinscrição dinâmica de tópicos
   - Suporte a múltiplas inscrições simultâneas
   - Recebimento de mensagens em tempo real (threading)
   - Filtro automático por tópico
   - Interface interativa com comandos

#### 4. **Exemplos e Demonstrações**
   - `demo.py`: Demonstração automática com múltiplos usuários
   - `exemplo_extensao.py`: Recursos avançados (JSON, prioridades, arquivos)
   - `test_sistema.py`: Testes automatizados

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    PUBLISHER (Servidor)                      │
│                      publisher.py                            │
│                                                              │
│  Tópicos: GERAL | TECNOLOGIA | ESPORTES | ENTRETENIMENTO    │
│           NOTICIAS | SISTEMA                                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ ZeroMQ PUB-SUB
                         │ tcp://localhost:5555
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌────────────┐  ┌────────────┐  ┌────────────┐
│ SUBSCRIBER │  │ SUBSCRIBER │  │ SUBSCRIBER │
│  (João)    │  │  (Maria)   │  │  (Pedro)   │
│            │  │            │  │            │
│ Inscrito:  │  │ Inscrito:  │  │ Inscrito:  │
│ - GERAL    │  │ - ESPORTES │  │ - TODOS    │
│ - TECH     │  │ - ENTRET.  │  │            │
└────────────┘  └────────────┘  └────────────┘
```

## 🎨 Principais Características

### 1. Desacoplamento
- Publisher não conhece os subscribers
- Subscribers não conhecem o publisher
- Comunicação baseada em tópicos

### 2. Escalabilidade
- Suporta múltiplos subscribers simultâneos
- Adição/remoção dinâmica de clientes
- Sem necessidade de reconfiguração do servidor

### 3. Filtro de Mensagens
- Cada subscriber recebe apenas mensagens dos tópicos inscritos
- Reduz tráfego de rede e processamento
- Implementado nativamente pelo ZeroMQ

### 4. Assincronismo
- Publisher não espera confirmação
- Subscribers recebem mensagens independentemente
- Comunicação não-bloqueante

## 📊 Conceitos de Sistemas Distribuídos Demonstrados

### ✅ Padrão Publish-Subscribe
- Desacoplamento entre produtor e consumidor
- Comunicação um-para-muitos (1:N)
- Baseado em tópicos/eventos

### ✅ Comunicação Assíncrona
- Mensagens enviadas sem bloqueio
- Recebimento independente por cada subscriber
- Threading para recebimento contínuo

### ✅ Sistemas Baseados em Eventos
- Notificações por tópicos
- Inscrição seletiva em eventos
- Distribuição eficiente de informações

### ✅ Middleware de Mensagens
- ZeroMQ como camada de comunicação
- Abstração do protocolo de rede
- Gerenciamento automático de conexões

## 🔧 Tecnologias Utilizadas

- **Python 3.x**: Linguagem de programação
- **ZeroMQ (pyzmq)**: Biblioteca de mensagens assíncronas
- **Threading**: Para recebimento simultâneo de mensagens
- **JSON**: Para mensagens estruturadas (exemplo avançado)

## 📚 Estrutura do Código

### Classe ChatPublisher
```python
- __init__(): Inicialização do socket PUB
- send_message(): Enviar mensagem para tópico
- send_system_message(): Mensagens do sistema
- broadcast_to_all(): Enviar para todos os tópicos
- run_interactive_mode(): Modo interativo
- run_automatic_mode(): Modo automático
```

### Classe ChatSubscriber
```python
- __init__(): Inicialização do socket SUB
- subscribe_to_topic(): Inscrever em tópico
- unsubscribe_from_topic(): Cancelar inscrição
- receive_messages(): Thread de recebimento
- run_interactive(): Modo interativo com comandos
- run_simple(): Modo simples de recebimento
```

## 🎓 Casos de Uso Implementados

### 1. Chat em Grupo
- Usuários se inscrevem em grupos de interesse
- Mensagens são filtradas por tópico
- Suporta múltiplos grupos simultâneos

### 2. Sistema de Notificações
- Tópico SISTEMA para avisos gerais
- Todos os usuários recebem mensagens do sistema
- Usado para avisos importantes

### 3. Discussões Temáticas
- Cada tópico representa uma área de interesse
- Usuários participam apenas dos temas de interesse
- Reduz ruído de informação

### 4. Broadcast Administrativo
- Administrador pode enviar para todos os tópicos
- Útil para avisos urgentes
- Comando especial no publisher

## 🚀 Como Funciona

### Fluxo de Execução

1. **Inicialização do Publisher**
   ```python
   socket = context.socket(zmq.PUB)
   socket.bind("tcp://localhost:5555")
   ```

2. **Conexão dos Subscribers**
   ```python
   socket = context.socket(zmq.SUB)
   socket.connect("tcp://localhost:5555")
   socket.setsockopt_string(zmq.SUBSCRIBE, "TECNOLOGIA")
   ```

3. **Envio de Mensagens**
   ```python
   message = "TECNOLOGIA [14:30] User: Olá!"
   socket.send_string(message)
   ```

4. **Recebimento Filtrado**
   ```python
   # Apenas mensagens que começam com "TECNOLOGIA"
   message = socket.recv_string()
   ```

## 🎯 Diferencial deste Projeto

### Além do Básico
- ✅ Interface interativa amigável
- ✅ Gerenciamento dinâmico de tópicos
- ✅ Múltiplos modos de operação
- ✅ Demonstrações automáticas
- ✅ Exemplos avançados
- ✅ Testes automatizados
- ✅ Documentação completa
- ✅ Código bem estruturado e comentado

### Extensibilidade
- Fácil adicionar novos tópicos
- Suporte a mensagens estruturadas (JSON)
- Possibilidade de prioridades
- Compartilhamento de arquivos (exemplo)
- Enquetes/votações (exemplo)

## 📖 Documentação Fornecida

1. **README.md**: Documentação completa com exemplos
2. **GUIA_RAPIDO.md**: Início rápido em 3 passos
3. **SOBRE_O_PROJETO.md**: Este arquivo (visão geral)
4. Comentários detalhados no código
5. Exemplos de uso práticos

## 🎉 Conclusão

Este projeto demonstra de forma prática e completa:
- O padrão Publish-Subscribe
- Comunicação distribuída com ZeroMQ
- Filtro de mensagens por tópico
- Escalabilidade e desacoplamento
- Aplicação real: sistema de chat em grupo

Todos os requisitos da atividade foram atendidos, com diversas funcionalidades extras que demonstram compreensão profunda dos conceitos de Sistemas Distribuídos.

---

**Desenvolvido para a disciplina de Sistemas Distribuídos**

