import socket
import json
import threading

UDP_IP = "0.0.0.0"  # Écoute toutes les interfaces
UDP_PORT = 14555  # Port d'écoute
BUFFER_SIZE = 1024  # Taille du buffer

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"🖥️ Serveur UDP en écoute sur {UDP_IP}:{UDP_PORT}")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)  # Réception des données
    decoded_data = data.decode('utf-8')  # Décodage en string
    latest_data = json.loads(decoded_data)  # Conversion en dictionnaire JSON
    print(f"📥 Données reçues de {addr}: {latest_data}")
