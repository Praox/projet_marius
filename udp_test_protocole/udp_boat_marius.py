import socket
import threading
import time

# Configuration
IP_BATEAU = "192.168.254.102"  # IP du bateau
PORT_UDP = 54325   # Port UDP pour envoyer les données
PORT_TCP = 54322  # Port TCP pour recevoir les commandes

# Création du socket UDP
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Création du socket TCP pour écouter les commandes
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind(("0.0.0.0", PORT_TCP))  # Écoute sur toutes les interfaces
tcp_sock.listen(1)

# 📌 Fonction pour envoyer des données en UDP
def envoyer_telemetrie():
    while True:
        message = "Vitesse: 50 km/h, Altitude: 100m"  # Exemple de télémétrie
        udp_sock.sendto(message.encode(), (IP_BATEAU, PORT_UDP))
        print(f"📡 Données envoyées : {message}")
        time.sleep(5)  # Envoi toutes les 2 secondes

# 📌 Fonction pour écouter les commandes TCP
def recevoir_commandes():
    print("🎧 En attente de connexion TCP du bateau...")
    conn, addr = tcp_sock.accept()
    print(f"✅ Connexion TCP établie avec {addr}")

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"🚀 Commande reçue : {data.decode()}")
        except:
            break
    
    conn.close()
    print("❌ Connexion TCP fermée")

# Lancement des threads
thread_udp = threading.Thread(target=envoyer_telemetrie)
thread_tcp = threading.Thread(target=recevoir_commandes)

thread_udp.start()
thread_tcp.start()
