import socket
import json
import threading

# --- CONFIGURATION ---

UDP_IP = "0.0.0.0"  # Écoute sur toutes les interfaces
UDP_PORT = 4000  # Port UDP
BUFFER_SIZE = 1024  # Taille du buffer

# Adresse du serveur TCP
TCP_IP = "192.168.254.120"
TCP_PORT = 3000

# Adresse Udp local
UDP_SEND_IP = "127.0.0.1"  # Adresse du serveur UDP
UDP_SEND_PORT_NETWORK = 4002  # Port d'envoi des données

# Flag d'arrêt
stop_flag = False

# Stockage des dernières données reçues
latest_data = {}




def calcul_traj(latest_data):
    # Exemple de calculs en utilisant acc['x']
    acc_x = latest_data.get('imu', {}).get('acc', {}).get('x', None)

    if acc_x is None:
        print("❌ Données manquantes pour le calcul de la trajectoire.")
        return None  # Retourne None ou une valeur par défaut si les données sont manquantes

    # Par exemple, supposons que l'on effectue un calcul basé sur acc_x.
    # Calcul du cap ou d'un autre paramètre avec acc_x.
    cap = acc_x  # Exemple de calcul (tu peux adapter avec d'autres formules si nécessaire)
    return cap

# --- FONCTION D'ENVOI UDP ---
def udp_forwarder():
    """Envoie les données calculées en UDP sur le réseau."""
    global latest_data
    while not stop_flag:
        if latest_data:  # Vérifie si les données sont disponibles
            cap = calcul_traj(latest_data)  # Calcule la trajectoire (ou cap)
            if cap is not None:
                try:
                    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    send_sock.sendto(str(cap).encode('utf-8'), (UDP_SEND_IP, UDP_SEND_PORT_NETWORK))  # Envoie les données calculées
                    print(f"📤 Données envoyées : {cap}")
                except Exception as e:
                    print(f"❌ Erreur lors de l'envoi des données : {e}")
        else:
            print("⚠️ Pas de données à envoyer, attend les nouvelles données UDP.")
        
        # Pour éviter une boucle trop rapide, on peut ajouter un petit délai
        threading.Event().wait(1)

# --- LANCEMENT DES THREADS UDP ---
udp_thread = threading.Thread(target=udp_listener, daemon=True)
tcp_thread = threading.Thread(target=tcp_listener, daemon=True)  # TCP tourne en arrière-plan
udp_forwarder_thread = threading.Thread(target=udp_forwarder, daemon=True)  # Envoi des données calculées
udp_thread.start()
tcp_thread.start()
udp_forwarder_thread.start()

# Maintenir le script en vie
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nInterruption détectée, arrêt des serveurs.")
    stop_flag = True
