import socket
import threading

# Configuration
IP_DRONE = "192.168.254.101"  # IP du drone
PORT_UDP = 12345  # Port UDP pour recevoir les données
PORT_TCP = 54321  # Port TCP pour envoyer les commandes

# Création du socket UDP pour recevoir les données du drone
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind(("0.0.0.0", PORT_UDP))  # Écoute sur toutes les interfaces

# 📌 Fonction pour recevoir la télémétrie
def recevoir_telemetrie():
    while True:
        data, addr = udp_sock.recvfrom(1024)
        print(f"📩 Télémétrie reçue de {addr}: {data.decode()}")

# 📌 Fonction pour envoyer des commandes en TCP
def envoyer_commandes():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((IP_DRONE, PORT_TCP))
    print(f"✅ Connexion TCP établie avec le drone ({IP_DRONE})")

    while True:
        commande = input("💬 Entrez une commande pour le drone : ")
        tcp_sock.send(commande.encode())

# Lancement des threads
thread_udp = threading.Thread(target=recevoir_telemetrie)
thread_tcp = threading.Thread(target=envoyer_commandes)

thread_udp.start()
thread_tcp.start()
