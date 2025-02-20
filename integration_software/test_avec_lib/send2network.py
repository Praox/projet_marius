import threading
import udp_utils  # Importer le module personnalisé

# --- CONFIGURATION ---
UDP_LISTEN_IP = "0.0.0.0"
UDP_LISTEN_PORT_SENSORS = 4001
UDP_LISTEN_PORT_TRAJ = 4002

UDP_SEND_IP = "192.168.254.115"
UDP_SEND_PORT = 14555

# --- CALLBACK POUR LE TRAITEMENT DES DONNÉES ---
def process_and_forward(data):
    """Callback pour traiter et forwarder les données UDP"""
    udp_utils.udp_forwarder(data, (UDP_SEND_IP, UDP_SEND_PORT))

# --- LANCEMENT DES THREADS UDP ---
udp_thread_sensors = threading.Thread(
    target=udp_utils.udp_listener,
    args=(UDP_LISTEN_IP, UDP_LISTEN_PORT_SENSORS, process_and_forward),
    daemon=True
)

udp_thread_traj = threading.Thread(
    target=udp_utils.udp_listener,
    args=(UDP_LISTEN_IP, UDP_LISTEN_PORT_TRAJ, process_and_forward),
    daemon=True
)

udp_thread_sensors.start()
udp_thread_traj.start()

# Maintenir le script en vie
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\n🛑 Arrêt du serveur UDP.")
