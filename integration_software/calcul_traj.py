import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 4000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((TCP_IP, TCP_PORT))
    server.listen()
    print(f"🖥️ Serveur TCP en écoute sur {TCP_IP}:{TCP_PORT}")

    conn, addr = server.accept()
    with conn:
        print(f"📩 Connexion depuis {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"📥 Données reçues : {data.decode('utf-8')}")
