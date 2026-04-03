import socket
import threading
import json
from datetime import datetime

BUFFER = 1024

# ===== CONFIGURAÇÃO DO NÓ =====
nome = input("Nome do nó (ex: No_A): ")
ip = "127.0.0.1"
porta = int(input("Porta deste nó: "))

# vizinhos
vizinhos = {
    "No_A": ("127.0.0.1", 5001),
    "No_B": ("127.0.0.1", 5002),
    "No_C": ("127.0.0.1", 5003)
}

# remover ele mesmo da lista
if nome in vizinhos:
    vizinhos.pop(nome)

mensagens_recebidas = []

# ===== RECEBER MENSAGENS =====
def receber_mensagens(sock):
    while True:
        data, addr = sock.recvfrom(BUFFER)

        mensagem = json.loads(data.decode())

        timestamp = mensagem["timestamp"]
        remetente = mensagem["remetente"]
        conteudo = mensagem["conteudo"]
        encaminhado = mensagem["encaminhado"]

        if encaminhado:
            print(f"\n📩 [{timestamp}] Encaminhado por {remetente}: {conteudo}")
        else:
            print(f"\n📩 [{timestamp}] {remetente}: {conteudo}")

        mensagens_recebidas.append(mensagem)

        print("\n>> ", end="")

# ===== ENVIAR MENSAGEM =====
def enviar_mensagem(sock):

    print("\nVizinhos disponíveis:")
    for v in vizinhos:
        print("-", v)

    destino = input("\nEnviar para: ")

    if destino not in vizinhos:
        print("❌ Nó inválido")
        return

    conteudo = input("Mensagem: ")

    mensagem = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "remetente": nome,
        "ip": ip,
        "porta": porta,
        "destino": destino,
        "conteudo": conteudo,
        "encaminhado": False
    }

    sock.sendto(json.dumps(mensagem).encode(), vizinhos[destino])

    print("✅ Mensagem enviada!")

# ===== ENCAMINHAR MENSAGEM =====
def encaminhar_mensagem(sock):

    if len(mensagens_recebidas) == 0:
        print("Nenhuma mensagem para encaminhar.")
        return

    print("\nMensagens recebidas:")

    for i, msg in enumerate(mensagens_recebidas):
        print(f"{i} - {msg['remetente']}: {msg['conteudo']}")

    escolha = int(input("Escolha a mensagem: "))

    msg = mensagens_recebidas[escolha]

    destino = input("Encaminhar para (No_A / No_B / No_C): ")

    if destino not in vizinhos:
        print("Destino inválido.")
        return

    nova_msg = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "remetente": nome,
        "ip": ip,
        "porta": porta,
        "destino": destino,
        "conteudo": f"[Mensagem original de {msg['remetente']}] {msg['conteudo']}",
        "encaminhado": True
    }

    sock.sendto(json.dumps(nova_msg).encode(), vizinhos[destino])

# ===== MENU =====
def menu(sock):

    while True:
        print("\n====== MENU ======")
        print("1 - Enviar mensagem")
        print("2 - Encaminhar mensagem")
        print("3 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            enviar_mensagem(sock)

        elif opcao == "2":
            encaminhar_mensagem(sock)

        elif opcao == "3":
            break

        else:
            print("Opção inválida")

# ===== MAIN =====
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, porta))

print(f"✅ {nome} rodando em {ip}:{porta}")

thread_receber = threading.Thread(target=receber_mensagens, args=(sock,))
thread_receber.daemon = True
thread_receber.start()

menu(sock)