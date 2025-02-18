import socket
import threading
from pymavlink import mavutil

# --- CONFIGURATION ---
# Adresse de l'antenne réceptrice UDP
RECEIVER_IP = "192.168.254.115"
RECEIVER_PORT = 14555
ADDR = (RECEIVER_IP, RECEIVER_PORT)

# Adresse du serveur TCP (pour arrêt distant)
TCP_IP = "192.168.254.120"
TCP_PORT = 3000

# Port Pixhawk
PIXHAWK_PORT = "/dev/ttyACM0"  # Modifier si nécessaire (ex: /dev/ttyUSB0 ou COM3 sous Windows)
BAUDRATE = 115200  # Vitesse de communication

# Flag d'arrêt
stop_flag = False

# --- CONNEXION À LA PIXHAWK ---
print(f"Connexion à la Pixhawk sur {PIXHAWK_PORT} à {BAUDRATE} bauds...")
master = mavutil.mavlink_connection(PIXHAWK_PORT, baud=BAUDRATE)
master.wait_heartbeat()
print("✅ Connexion établie avec la Pixhawk!")

# Demander les flux de données IMU
master.mav.request_data_stream_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_RAW_SENSORS,
    10,  # Fréquence de 10 Hz
    1
)


# --- FONCTION D'ENVOI UDP ---
def udp_sender():
    global stop_flag
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("📡 Transmission des données Pixhawk via UDP...")

    while not stop_flag:
        msg = master.recv_match(type=['RAW_IMU', 'SCALED_IMU2', 'SCALED_IMU3', 'ATTITUDE'], blocking=True)
        
        if msg:
            msg_type = msg.get_type()
            data = ""

            if msg_type in ['RAW_IMU', 'SCALED_IMU2', 'SCALED_IMU3']:
                data = f"{msg_type} | Accélération: x={msg.xacc}, y={msg.yacc}, z={msg.zacc} | " \
                       f"Gyroscope: x={msg.xgyro}, y={msg.ygyro}, z={msg.zgyro} | " \
                       f"Magnétomètre: x={msg.xmag}, y={msg.ymag}, z={msg.zmag}"
            
            elif msg_type == 'ATTITUDE':
                data = f"ATTITUDE | Roll={msg.roll:.2f}, Pitch={msg.pitch:.2f}, Yaw={msg.yaw:.2f}"

            sock.sendto(data.encode('utf-8'), ADDR)
            print(f"📤 Données envoyées : {data}")

    sock.close()
    print("📴 Transmission UDP arrêtée.")


# --- FONCTION DE RÉCEPTION TCP ---
def tcp_listener():
    global stop_flag
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind((TCP_IP, TCP_PORT))
    serveur.listen()

    print(f"🖥️ Serveur TCP en écoute sur {TCP_IP}:{TCP_PORT}...")

    while not stop_flag:
        try:
            client, infosclient = serveur.accept()
            request = client.recv(1024)
            message = request.decode('utf-8').strip()

            print(f"📩 Message TCP reçu : {message} de {infosclient[0]}")

            if message.lower() == "stop":
                print("🛑 Message d'arrêt reçu, arrêt de l'émission UDP.")
                stop_flag = True  # Active le flag pour stopper l'UDP

            client.close()
        except Exception as e:
            print(f"❌ Erreur TCP : {e}")
            break

    serveur.close()
    print("📴 Serveur TCP fermé.")


# --- LANCEMENT DES THREADS ---
udp_thread = threading.Thread(target=udp_sender)
tcp_thread = threading.Thread(target=tcp_listener, daemon=True)  # TCP tourne en arrière-plan

udp_thread.start()
tcp_thread.start()

try:
    udp_thread.join()  # Attendre la fin de l'UDP
except KeyboardInterrupt:
    print("\n🛑 Interruption détectée, arrêt des serveurs.")
    stop_flag = True

print("🏁 Programme terminé.")
