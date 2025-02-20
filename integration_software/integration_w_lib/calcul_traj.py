import threading
import json
import tools

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

# Liste des destinations UDP
UDP_DESTINATIONS = [
    (UDP_SEND_IP, UDP_SEND_PORT_NETWORK )]

# Flag d'arrêt
stop_flag = False

# Stockage des dernières données reçues
latest_data = {}

# --- CALLBACK POUR LE TRAITEMENT DES DONNÉES ---
def process_and_forward(data):
    """Callback pour traiter et forwarder les données UDP"""
    global latest_data
    try:
        latest_data = tools.json.loads(data)  # Assure-toi que 'data' est bien un JSON
        cap = calcul_traj(latest_data)  
        if cap is not None:  
            tools.udp_forwarder(cap, UDP_DESTINATIONS)
    except json.JSONDecodeError:
        print("❌ Erreur : données reçues mal formatées")



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

# --- LANCEMENT DES THREADS UDP ---
udp_thread = threading.Thread(
    target=tools.udp_listener,
    args=(UDP_IP, UDP_PORT, process_and_forward),
    daemon=True
)
tcp_thread = threading.Thread(
    target=tools.tcp_listener,
    args= (TCP_IP, TCP_PORT),
    daemon=True
)

# --- LANCEMENT DES THREADS UDP ---
udp_thread.start()
try:
    tcp_thread.start()
except Exception as e:
    print(f"❌ Erreur lors du démarrage du serveur TCP : {e}")



# Maintenir le script en vie
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nInterruption détectée, arrêt des serveurs.")
    stop_flag = True
