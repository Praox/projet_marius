import socket
import threading
from pymavlink import mavutil

# --- CONFIGURATION ---
# Adresse de l'antenne réceptrice UDP
RECEIVER_IP = "192.168.254.115"
RECEIVER_PORT = 14555
ADDR = (RECEIVER_IP, RECEIVER_PORT)

# Port Pixhawk
PIXHAWK_PORT = "/dev/ttyACM0"  # Modifier selon ton matériel
BAUDRATE_PIXHAWK = 115200  # Vitesse de la Pixhawk

# Port GPS NMEA
GPS_PORT = "/dev/ttyUSB0"  # Modifier selon ton matériel
BAUDRATE_GPS = 4800  # Baudrate du GPS NMEA


# --- CONNEXION À LA PIXHAWK ---
print(f"Connexion à la Pixhawk sur {PIXHAWK_PORT} à {BAUDRATE_PIXHAWK} bauds...")
master = mavutil.mavlink_connection(PIXHAWK_PORT, baud=BAUDRATE)
master.wait_heartbeat()
print("✅ Connexion établie avec la Pixhawk!")

# Demande des flux de données IMU
master.mav.request_data_stream_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_RAW_SENSORS,
    10,  # Fréquence de 10 Hz
    1
)

# --- FONCTION DE DÉCODAGE DES DONNÉES ---
def decode_sensors():
    """
    Lit les données de la Pixhawk et retourne un dictionnaire contenant 
    les valeurs IMU et NMEA (si disponibles).
    """
    msg = master.recv_match(type=['RAW_IMU', 'SCALED_IMU2', 'SCALED_IMU3', 'ATTITUDE', 'GPS_RAW_INT'], blocking=True)
    if not msg:
        return None

    sensor_data = {}
    msg_type = msg.get_type()

    if msg_type in ['RAW_IMU', 'SCALED_IMU2', 'SCALED_IMU3']:
        sensor_data = {
            "type": msg_type,
            "accX": msg.xacc,
            "accY": msg.yacc,
            "accZ": msg.zacc,
            "gyroX": msg.xgyro,
            "gyroY": msg.ygyro,
            "gyroZ": msg.zgyro,
            "magX": msg.xmag,
            "magY": msg.ymag,
            "magZ": msg.zmag
        }
    
    elif msg_type == 'ATTITUDE':
        sensor_data = {
            "type": "ATTITUDE",
            "roll": round(msg.roll, 2),
            "pitch": round(msg.pitch, 2),
            "yaw": round(msg.yaw, 2)
        }
    
    elif msg_type == 'GPS_RAW_INT':  # Données GPS en format NMEA
        sensor_data = {
            "type": "GPS",
            "lat": msg.lat / 1e7,
            "lon": msg.lon / 1e7,
            "alt": msg.alt / 1e3,
            "speed": msg.vel / 100,
            "satellites": msg.satellites_visible
        }

    return sensor_data

# --- FONCTION D'ENVOI UDP ---
def udp_sender():
    """
    Envoie les données décodées en UDP sur le réseau local.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"📡 Transmission des données Pixhawk via UDP à {RECEIVER_IP}:{RECEIVER_PORT}...")

    while True:
        sensor_data = decode_sensors()
        if sensor_data:
            data_str = str(sensor_data)  # Convertir en chaîne de caractères
            sock.sendto(data_str.encode('utf-8'), ADDR)
            print(f"📤 Données envoyées : {data_str}")

    sock.close()
    print("📴 Transmission UDP arrêtée.")

# --- LANCEMENT DU THREAD UDP ---
udp_thread = threading.Thread(target=udp_sender)
udp_thread.start()

try:
    udp_thread.join()  # Attendre la fin de l'UDP
except KeyboardInterrupt:
    print("\n🛑 Interruption détectée, arrêt du programme.")

print("🏁 Programme terminé.")
