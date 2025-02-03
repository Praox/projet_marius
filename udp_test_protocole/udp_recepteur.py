import socket
import json

# Adresse IP d'écoute et le port
LISTEN_IP = "0.0.0.0"  # L'ordinateur récepteur écoute sur toutes les interfaces réseau
#LISTEN_IP = "192.168.254.115"  # L'ordinateur récepteur écoute sur toutes les interfaces réseau
#LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 14555

# Création du socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print(f"Récepteur UDP en attente de messages sur {LISTEN_IP}:{LISTEN_PORT}...")

while True:
    data0, addr = sock.recvfrom(1024)  # Réception des données (max 1024 octets)
    print("data received : ", data0)
    data = data0.decode('utf-8')
    print(f"Message reçu de {addr}: {data}")
