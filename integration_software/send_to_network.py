import socket
import json
import threading

# --- CONFIGURATION ---
UDP_LISTEN_IP = "0.0.0.0"  # Écoute sur toutes les interfaces
UDP_LISTEN_PORT_SENSORS = 4001  # Port d'écoute UDP pour les capteurs
UDP_LISTEN_PORT_TRAJ = 4002  # Port d'écoute UDP pour les trajectoires
BUFFER_SIZE = 1024  # Taille du buffer

# Adresse de destination pour l'envoi des données
UDP_SEND_IP = "192.168.254.115"  # Adresse de ton PC sur le réseau privé
UDP_SEND_PORT = 14555  # Port de réception sur ton PC

# Stockage des dernières données reçues
latest_data = {}

# --- SERVEUR UDP ---
def udp_listener_sensors():
    """Écoute les messages UDP entrants sur le port des capteurs et met à jour les dernières données."""
    global latest_data
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_LISTEN_IP, UDP_LISTEN_PORT_SENSORS))
    
    print(f"🖥️ Serveur UDP en écoute sur {UDP_LISTEN_IP}:{UDP_LISTEN_PORT_SENSORS}")

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

def udp_listener_traj():
    """Écoute les messages UDP entrants sur le port des trajectoires."""
    global latest_data
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_LISTEN_IP, UDP_LISTEN_PORT_TRAJ))
    
    print(f"🖥️ Serveur UDP en écoute sur {UDP_LISTEN_IP}:{UDP_LISTEN_PORT_TRAJ}")

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

# --- LANCEMENT DES THREADS UDP ---
udp_thread_sensors = threading.Thread(target=udp_listener_sensors, daemon=True)
udp_thread_traj = threading.Thread(target=udp_listener_traj, daemon=True)

# Démarrer les threads pour écouter sur les deux ports
udp_thread_sensors.start()
udp_thread_traj.start()

# Maintenir le script en vie
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\n🛑 Arrêt du serveur UDP.")
