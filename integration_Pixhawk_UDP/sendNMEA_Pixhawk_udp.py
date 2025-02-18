import socket
import threading
import serial
from pymavlink import mavutil
from pynmeagps import NMEAReader, NMEAMessage

# --- CONFIGURATION ---
# Adresse de l'antenne réceptrice UDP
RECEIVER_IP = "192.168.254.115"
RECEIVER_PORT = 14555
ADDR = (RECEIVER_IP, RECEIVER_PORT)

# Adresse du serveur TCP (pour arrêt distant)
TCP_IP = "192.168.254.120"
TCP_PORT = 3000

# Port Pixhawk
PIXHAWK_PORT = "/dev/ttyACM0"  # Modifier selon ton matériel
BAUDRATE_PIXHAWK = 115200  # Vitesse de la Pixhawk

# Port GPS NMEA
GPS_PORT = "/dev/ttyUSB0"  # Modifier selon ton matériel
BAUDRATE_GPS = 4800  # Baudrate du GPS NMEA

# Flag d'arrêt global
stop_flag = False

# --- CONNEXION À LA PIXHAWK ---
print(f"Connexion à la Pixhawk sur {PIXHAWK_PORT} à {BAUDRATE_PIXHAWK} bauds...")
master = mavutil.mavlink_connection(PIXHAWK_PORT, baud=BAUDRATE_PIXHAWK)
master.wait_heartbeat()
print("✅ Connexion établie avec la Pixhawk!")

# Demander les flux de données IMU
master.mav.request_data_stream_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_RAW_SENSORS,
    10,  # Fréquence en Hz
    1
)

# --- FONCTION D'ENVOI UDP (PIXHAWK + GPS) ---
def udp_sender():
    global stop_flag
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("📡 Transmission des données Pixhawk et GPS via UDP...")

    while not stop_flag:
        # Lire les données IMU de la Pixhawk
        msg = master.recv_match(type=['RAW_IMU', 'SCALED_IMU2', 'SCALED_IMU3', 'ATTITUDE'], blocking=True)
        imu_data = ""

        if msg:
            msg_type = msg.get_type()
            if msg_type in ['RAW_IMU', 'SCALED_IMU2', 'SCALED_IMU3']:
                imu_data = f"{msg_type} | Acc: x={msg.xacc}, y={msg.yacc}, z={msg.zacc} | " \
                           f"Gyro: x={msg.xgyro}, y={msg.ygyro}, z={msg.zgyro} | " \
                           f"Mag: x={msg.xmag}, y={msg.ymag}, z={msg.zmag}"
            elif msg_type == 'ATTITUDE':
                imu_data = f"ATTITUDE | Roll={msg.roll:.2f}, Pitch={msg.pitch:.2f}, Yaw={msg.yaw:.2f}"

        # Lire les dernières données GPS
        gps_data = get_latest_gps_data()

        # Fusionner les données Pixhawk et GPS
        combined_data = f"{imu_data} || {gps_data}"
        sock.sendto(combined_data.encode('utf-8'), ADDR)
        print(f"📤 Données envoyées : {combined_data}")

    sock.close()
    print("📴 Transmission UDP arrêtée.")


# --- FONCTION DE LECTURE GPS NMEA ---
latest_gps_data = "GPS: Aucune donnée"

def get_latest_gps_data():
    """Retourne la dernière trame GPS stockée"""
    global latest_gps_data
    return latest_gps_data

def gps_reader():
    global latest_gps_data, stop_flag
    try:
        with serial.Serial(GPS_PORT, BAUDRATE_GPS, timeout=1) as ser:
            print(f"📡 Lecture des données GPS sur {GPS_PORT}...")
            nmea_reader = NMEAReader(ser)

            while not stop_flag:
                try:
                    (raw_data, parsed_data) = nmea_reader.read()
                    if isinstance(parsed_data, NMEAMessage):
                        if parsed_data.msgID == "GGA":  # Exemple pour GPGGA
                            latest_gps_data = f"GGA | Lat: {parsed_data.lat}, Lon: {parsed_data.lon}, Alt: {parsed_data.alt}"
                        elif parsed_data.msgID == "VTG":  # Exemple pour GPVTG
                            latest_gps_data = f"VTG | Vitesse: {parsed_data.spd_over_grnd_kmph} km/h"
                except Exception as e:
                    print(f"❌ Erreur GPS : {e}")
    except serial.SerialException as e:
        print(f"❌ Erreur d'accès au port GPS : {e}")

    print("📴 Lecture GPS arrêtée.")


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
                stop_flag = True  # Active le flag pour stopper l'UDP et GPS

            client.close()
        except Exception as e:
            print(f"❌ Erreur TCP : {e}")
            break

    serveur.close()
    print("📴 Serveur TCP fermé.")


# --- LANCEMENT DES THREADS ---
udp_thread = threading.Thread(target=udp_sender)
gps_thread = threading.Thread(target=gps_reader, daemon=True)  # GPS tourne en arrière-plan
tcp_thread = threading.Thread(target=tcp_listener, daemon=True)  # TCP tourne en arrière-plan

udp_thread.start()
gps_thread.start()
tcp_thread.start()

try:
    udp_thread.join()  # Attendre la fin de l'UDP
except KeyboardInterrupt:
    print("\n🛑 Interruption détectée, arrêt des serveurs.")
    stop_flag = True

print("🏁 Programme terminé.")
