import socket

# Adresse IP d'écoute et le port
LISTEN_IP = "0.0.0.0"  # Écoute sur toutes les interfaces réseau
LISTEN_PORT = 14555

# Création du socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print(f"Récepteur UDP en attente de messages sur {LISTEN_IP}:{LISTEN_PORT}...")

try:
    while True:
        data, addr = sock.recvfrom(1024)  # Réception des données (max 1024 octets)
        print(f"Message reçu de {addr}: {data.decode()}")

except KeyboardInterrupt:
    print("\nArrêt du récepteur.")
finally:
    sock.close()
