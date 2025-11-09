[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/mrIsNMKU)

# Sistema de Chat em Grupo com Publish-Subscribe usando ZeroMQ

Este é um sistema de chat em grupo baseado no padrão **Publish-Subscribe** implementado com **ZeroMQ**. Cada grupo corresponde a um tópico, permitindo que usuários se inscrevam em múltiplos grupos simultaneamente.

## 📋 Descrição

O sistema implementa um chat distribuído onde:
- **Publisher (Servidor)**: Envia mensagens para diferentes tópicos/grupos
- **Subscriber (Cliente)**: Recebe mensagens dos tópicos nos quais está inscrito
- **Tópicos disponíveis**: GERAL, TECNOLOGIA, ESPORTES, ENTRETENIMENTO, NOTICIAS, SISTEMA

## 🎯 Funcionalidades

### Publisher (Servidor de Chat)
- ✅ Modo interativo para enviar mensagens manualmente
- ✅ Modo automático para enviar mensagens periódicas
- ✅ Suporte a múltiplos tópicos/grupos
- ✅ Broadcast de mensagens para todos os tópicos
- ✅ Mensagens do sistema com timestamp
- ✅ Interface amigável com menus e comandos

### Subscriber (Cliente de Chat)
- ✅ Modo interativo com gerenciamento de inscrições
- ✅ Inscrição/desinscrição dinâmica de tópicos
- ✅ Suporte a múltiplas inscrições simultâneas
- ✅ Recebimento de mensagens em tempo real
- ✅ Filtro de mensagens por tópico
- ✅ Interface com emojis e formatação colorida

## ⚡ Início Rápido

**Novo na aplicação? Veja o [GUIA_RAPIDO.md](GUIA_RAPIDO.md) para começar em 3 passos!**

### Testar o Sistema

Antes de começar, você pode executar os testes automatizados:

```bash
python test_sistema.py
```

## 🔧 Instalação

### Windows (PowerShell)

1. **Instalar Python** (se ainda não tiver)
   - Baixe em: https://www.python.org/downloads/
   - Durante a instalação, marque "Add Python to PATH"

2. **Instalar ZeroMQ**
   ```powershell
   pip install pyzmq
   ```

### Linux/Ubuntu

```bash
# Opção 1: Instalação global
sudo apt update
sudo apt install python3-zmq

# Opção 2: Usando ambiente virtual (recomendado)
sudo apt update
sudo apt install python3-pip python3-venv
python3 -m venv myvenv
source myvenv/bin/activate
pip3 install pyzmq
```

## ⚙️ Configuração

Configure o endereço IP e porta do servidor no arquivo `constPS.py`:

```python
HOST = "localhost"  # Use "localhost" para teste local
PORT = "5555"       # Porta do servidor
```

Para testar em rede:
- Altere `HOST` para o IP da máquina que executará o publisher
- Certifique-se de que a porta está liberada no firewall

## 🚀 Como Usar

### 1. Iniciar o Servidor (Publisher)

Em um terminal, execute:

```bash
python publisher.py
```

Escolha o modo:
- **Modo 1 (Interativo)**: Permite enviar mensagens manualmente
  - Formato: `<número_tópico> <nome_usuario> <mensagem>`
  - Exemplo: `1 Admin Bem-vindos ao chat!`
  - Broadcast: `broadcast Usuario Mensagem para todos`

- **Modo 2 (Automático)**: Envia mensagens automáticas periodicamente

### 2. Iniciar o Cliente (Subscriber)

Em outro terminal (ou em outra máquina), execute:

```bash
python subscriber.py
```

Digite seu nome de usuário e escolha o modo:

- **Modo 1 (Interativo)**: Gerenciar inscrições dinamicamente
  - Comandos disponíveis:
    - `listar` - Ver todos os tópicos
    - `inscrever` - Inscrever em um tópico
    - `desinscrever` - Cancelar inscrição
    - `todos` - Inscrever em todos os tópicos
    - `inscritos` - Ver seus tópicos ativos
    - `ajuda` - Mostrar menu de comandos
    - `sair` - Encerrar o chat

- **Modo 2 (Simples)**: Recebe mensagens de todos os tópicos

- **Modo 3 (Personalizado)**: Escolhe tópicos iniciais

### 3. Múltiplos Clientes

Você pode executar vários subscribers simultaneamente:

```bash
# Terminal 1
python subscriber.py

# Terminal 2
python subscriber.py

# Terminal 3
python subscriber.py
```

Cada cliente pode se inscrever em tópicos diferentes!

## 📚 Exemplos de Uso

### Exemplo 1: Chat de Tecnologia

**Publisher:**
```
> 2 TechGuru Nova versão do Python lançada!
```

**Subscriber (inscrito em TECNOLOGIA):**
```
💬 TECNOLOGIA [14:30:25] TechGuru: Nova versão do Python lançada!
```

### Exemplo 2: Broadcast para Todos

**Publisher:**
```
> broadcast Admin Manutenção programada em 10 minutos
```

**Subscribers (todos os tópicos):**
```
💬 GERAL [14:35:00] Admin: Manutenção programada em 10 minutos
💬 TECNOLOGIA [14:35:00] Admin: Manutenção programada em 10 minutos
💬 ESPORTES [14:35:00] Admin: Manutenção programada em 10 minutos
...
```

### Exemplo 3: Gerenciamento Dinâmico de Tópicos

```
Comando > listar
Tópicos disponíveis:
  [✓] 1. GERAL
  [ ] 2. TECNOLOGIA
  [✓] 3. ESPORTES
  ...

Comando > inscrever
Número do tópico: 2
✓ Inscrito no tópico: TECNOLOGIA

Comando > inscritos
Tópicos inscritos:
  ✓ GERAL
  ✓ TECNOLOGIA
  ✓ ESPORTES
  ✓ SISTEMA
```

## 🔍 Arquivos do Projeto

### Arquivos Principais ⭐
- **`publisher.py`**: Publisher completo com sistema de chat por tópicos
- **`subscriber.py`**: Subscriber completo com múltiplos tópicos
- **`constPS.py`**: Configurações de host e porta

### Exemplos e Demonstrações
- **`demo.py`**: Demonstração automática com múltiplos usuários simulados
- **`exemplo_extensao.py`**: Exemplos avançados (JSON, prioridades, arquivos)
- **`test_sistema.py`**: Script de testes automatizados
- **`publisher_chat.py`**: Cópia do publisher (mesmo código de publisher.py)
- **`subscriber_chat.py`**: Cópia do subscriber (mesmo código de subscriber.py)

### Documentação
- **`README.md`**: Documentação completa
- **`GUIA_RAPIDO.md`**: Guia rápido de 3 passos
- **`COMO_EXECUTAR.txt`**: Guia visual passo a passo
- **`SOBRE_O_PROJETO.md`**: Visão geral técnica
- **`requirements.txt`**: Dependências do projeto

## 🎓 Conceitos de Sistemas Distribuídos

Este projeto demonstra:

1. **Padrão Publish-Subscribe**
   - Desacoplamento entre remetente e destinatário
   - Um-para-muitos (1:N)
   - Baseado em tópicos/grupos

2. **Comunicação Assíncrona**
   - Publisher não espera confirmação
   - Subscribers recebem mensagens de forma independente

3. **Escalabilidade**
   - Múltiplos subscribers podem se conectar
   - Adição/remoção dinâmica de clientes
   - Sem necessidade de reconfiguração do servidor

4. **Filtro de Mensagens**
   - Subscribers só recebem mensagens dos tópicos inscritos
   - Reduz tráfego de rede e processamento

## 🛠️ Troubleshooting

### Erro: "Address already in use"
- O publisher já está rodando em outra instância
- Aguarde alguns segundos ou mude a porta em `constPS.py`

### Erro: "Connection refused"
- Verifique se o publisher está rodando
- Confirme o endereço IP e porta em `constPS.py`
- Verifique o firewall

### Mensagens não aparecem
- Certifique-se de estar inscrito em pelo menos um tópico
- O tópico SISTEMA é sempre recomendado
- Aguarde alguns segundos após a conexão inicial

### No Windows: "zmq not found"
- Reinstale: `pip uninstall pyzmq` e depois `pip install pyzmq`
- Verifique se está usando o Python correto: `python --version`

## 📖 Referência

Baseado no exemplo da Figura 4.22 do livro de Sistemas Distribuídos, com melhorias e novas funcionalidades:
- Sistema de chat em grupo
- Interface interativa
- Múltiplos tópicos
- Gerenciamento dinâmico de inscrições
- Mensagens com timestamp
- Modos de operação variados

## 👥 Contribuições

Este projeto foi desenvolvido como parte da disciplina de Sistemas Distribuídos.

---

**Desenvolvido com ZeroMQ** 🚀
