import socket
import json
import threading

# --- CONFIGURATION ---
UDP_IP = "0.0.0.0"  # Écoute sur toutes les interfaces
UDP_PORT = 4000  # Port UDP
BUFFER_SIZE = 1024  # Taille du buffer

# Stockage des dernières données reçues
latest_data = {}

# --- SERVEUR UDP ---
def udp_listener():
    """Écoute les messages UDP entrants et met à jour les dernières données."""
    global latest_data
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    print(f"🖥️ Serveur UDP en écoute sur {UDP_IP}:{UDP_PORT}")

    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)  # Réception des données
            decoded_data = data.decode('utf-8')  # Décodage en string
            latest_data = json.loads(decoded_data)  # Conversion en dictionnaire JSON
            
            print(f"📥 Données reçues de {addr}: {latest_data}")

        except json.JSONDecodeError:
            print("❌ Erreur : données reçues mal formatées")
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")

# --- LANCEMENT DU THREAD UDP ---
udp_thread = threading.Thread(target=udp_listener, daemon=True)
udp_thread.start()

# Maintenir le script en vie
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\n🛑 Arrêt du serveur UDP.")
