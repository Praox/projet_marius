import socket

UDP_IP = "0.0.0.0"  # Écoute toutes les interfaces
UDP_PORT = 5000  # Port d'écoute

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"🖥️ Serveur UDP en écoute sur {UDP_IP}:{UDP_PORT}")

while True:
    data, addr = sock.recvfrom(1024)  # Réception des données
    print(f"📥 Données reçues de {addr}: {data.decode('utf-8')}")
