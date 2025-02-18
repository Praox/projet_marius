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

# Flag d'arrêt
stop_flag = False

# Stockage des dernières données reçues
latest_data = {}

# --- SERVEUR UDP ---
def udp_listener():
    """Écoute les messages UDP entrants et met à jour les dernières données."""
    global latest_data
    global stop_flag
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    print(f"🖥️ Serveur UDP en écoute sur {UDP_IP}:{UDP_PORT}")

    while not stop_flag:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)  # Réception des données
            decoded_data = data.decode('utf-8')  # Décodage en string
            latest_data = json.loads(decoded_data)  # Conversion en dictionnaire JSON
            
            print(f"📥 Données reçues de {addr}: {latest_data}")

        except json.JSONDecodeError:
            print("❌ Erreur : données reçues mal formatées")
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")

# Fonction de réception TCP (tourne en boucle infinie)
def tcp_listener():
    global stop_flag
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind((TCP_IP, TCP_PORT))
    serveur.listen()

    print(f"Serveur TCP en écoute sur {TCP_IP}:{TCP_PORT}...")

    while not stop_flag:
        try:
            client, infosclient = serveur.accept()
            request = client.recv(1024)
            message = request.decode('utf-8').strip()
            
            print(f"Message TCP reçu : {message}")
            print(f"IP client connecté : {infosclient[0]}")
            
            if message.lower() == "stop":
                print("Message d'arrêt reçu, arrêt de l'émission UDP.")
                stop_flag = True  # Active le flag pour stopper l'UDP
            
            client.close()
        except Exception as e:
            print(f"Erreur TCP : {e}")
            break

    serveur.close()
    print("Serveur TCP fermé.")

# --- LANCEMENT DU THREAD UDP ---
udp_thread = threading.Thread(target=udp_listener, daemon=True)
tcp_thread = threading.Thread(target=tcp_listener, daemon=True)  # TCP tourne en arrière-plan
udp_thread.start()
tcp_thread.start()


# Maintenir le script en vie
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nInterruption détectée, arrêt des serveurs.")
    stop_flag = True
