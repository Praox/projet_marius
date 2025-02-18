import socket
import json
import threading

# --- CONFIGURATION ---
UDP_LISTEN_IP = "0.0.0.0"  # Écoute sur toutes les interfaces
UDP_LISTEN_PORT = 4000  # Port d'écoute UDP en local
BUFFER_SIZE = 1024  # Taille du buffer

# Adresse de destination pour l'envoi des données
UDP_SEND_IP = "192.168.254.115"  # Adresse de ton PC sur le réseau privé
UDP_SEND_PORT = 14555  # Port de réception sur ton PC

# Stockage des dernières données reçues
latest_data = {}

# --- SERVEUR UDP ---
def udp_listener():
    """Écoute les messages UDP entrants et met à jour les dernières données."""
    global latest_data
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_LISTEN_IP, UDP_LISTEN_PORT))
    
    print(f"🖥️ Serveur UDP en écoute sur {UDP_LISTEN_IP}:{UDP_LISTEN_PORT}")

    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)  # Réception des données
            decoded_data = data.decode('utf-8')  # Décodage en string
            latest_data = json.loads(decoded_data)  # Conversion en dictionnaire JSON
            
            print(f"📥 Données reçues de {addr}: {latest_data}")
            
            # Envoyer immédiatement les données sur le réseau privé
            udp_forwarder(decoded_data)

        except json.JSONDecodeError:
            print("❌ Erreur : données reçues mal formatées")
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")

# --- FONCTION D'ENVOI UDP ---
def udp_forwarder(data):
    """Transmet les données reçues en UDP vers un autre appareil."""
    try:
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        send_sock.sendto(data.encode('utf-8'), (UDP_SEND_IP, UDP_SEND_PORT))
        print(f"📤 Données envoyées à {UDP_SEND_IP}:{UDP_SEND_PORT}")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi des données : {e}")

        

# --- LANCEMENT DU THREAD UDP ---
udp_thread = threading.Thread(target=udp_listener, daemon=True)
udp_thread.start()

# Maintenir le script en vie
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\n🛑 Arrêt du serveur UDP.")
