import socket
import threading

HOST = "127.0.0.1"

def receber_mensagens(conn, addr):
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"\n📩 Mensagem de {addr[1]}: {msg}\n>> ", end="")
        except:
            break

def iniciar_servidor(porta):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, porta))
    servidor.listen()

    print(f"✅ Usuário rodando na porta {porta}...")

    while True:
        conn, addr = servidor.accept()
        thread = threading.Thread(target=receber_mensagens, args=(conn, addr))
        thread.start()

def enviar_mensagem(minha_porta):
    while True:
        try:
            destino = input("\n📤 Porta destino (5001/5002/5003): ").strip()

            if not destino.isdigit():
                print("❌ Porta inválida!")
                continue

            destino = int(destino)

            msg = input("✏️ Mensagem: ").strip()

            if msg == "":
                print("❌ Mensagem vazia!")
                continue

            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((HOST, destino))

            mensagem_formatada = f"[{minha_porta}] {msg}"
            cliente.send(mensagem_formatada.encode())

            cliente.close()

        except Exception as e:
            print(f"❌ Erro: {e}")

# ===== MAIN =====
porta = int(input("🚀 Porta deste usuário: "))

threading.Thread(target=iniciar_servidor, args=(porta,), daemon=True).start()

enviar_mensagem(porta)