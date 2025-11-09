# 🚀 Guia Rápido de Uso

## Instalação Rápida

```bash
# Instalar dependências
pip install -r requirements.txt

# OU
pip install pyzmq
```

## Uso Básico - 3 Passos

### 1️⃣ Iniciar o Servidor

```bash
python publisher.py
```

Escolha o modo 1 (Interativo) para enviar mensagens manualmente.

### 2️⃣ Iniciar um Cliente (em outro terminal)

```bash
python subscriber.py
```

Digite seu nome e escolha o modo 1 (Interativo).

### 3️⃣ Começar a Conversar!

**No Publisher:**
```
> 1 Admin Bem-vindos ao chat!
```

**No Subscriber:**
```
Comando > todos
✓ Inscrito em todos os tópicos

💬 GERAL [14:30:25] Admin: Bem-vindos ao chat!
```

## 🎯 Comandos Úteis do Subscriber

```
listar       - Ver todos os tópicos
inscrever    - Entrar em um tópico
todos        - Entrar em todos os tópicos
inscritos    - Ver seus tópicos ativos
sair         - Sair do chat
```

## 🎬 Ver Demonstração Automática

```bash
python demo.py
```

Mostra o sistema funcionando com múltiplos usuários simulados!

## 📚 Ver Exemplos Avançados

```bash
python exemplo_extensao.py
```

Demonstra recursos avançados como:
- Mensagens estruturadas (JSON)
- Prioridades
- Compartilhamento de arquivos
- Enquetes

## 🔧 Tópicos Disponíveis

1. **GERAL** - Chat geral para todos
2. **TECNOLOGIA** - Discussões sobre tech
3. **ESPORTES** - Notícias e discussões esportivas
4. **ENTRETENIMENTO** - Filmes, música, séries
5. **NOTICIAS** - Notícias importantes
6. **SISTEMA** - Mensagens do sistema (sempre ativo)

## 💡 Dicas

- Abra múltiplos terminais para simular vários usuários
- Cada usuário pode escolher tópicos diferentes
- Mensagens são filtradas automaticamente por tópico
- Use `broadcast` no publisher para enviar a todos os tópicos

## 🐛 Problemas Comuns

**"Address already in use"**
- Já existe um publisher rodando
- Feche-o ou mude a porta em `constPS.py`

**"Connection refused"**
- O publisher não está rodando
- Inicie o publisher primeiro

**Não recebo mensagens**
- Inscreva-se em pelo menos um tópico
- Use o comando `todos` para garantir

## 📖 Mais Informações

Veja o [README.md](README.md) completo para documentação detalhada.

---

**Divirta-se explorando o Publish-Subscribe com ZeroMQ! 🎉**

