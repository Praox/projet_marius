from pymavlink import mavutil

# --- CONFIGURATION ---
PORT = "/dev/ttyACM0"  # Change selon ton port (ex: /dev/ttyUSB0 ou COM3 sous Windows)
BAUDRATE = 115200  # Vitesse de communication

# Connexion à la Pixhawk
print(f"Connexion à {PORT} en {BAUDRATE} bauds...")
master = mavutil.mavlink_connection(PORT, baud=BAUDRATE)

# Attendre un heartbeat pour s'assurer que la connexion est établie
print("Attente du heartbeat de la Pixhawk...")
master.wait_heartbeat()
print("✅ Connexion établie avec la Pixhawk!")

# --- DEMANDER LES FLUX DE DONNÉES ---
# Activer l'envoi des données IMU brutes
master.mav.request_data_stream_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_RAW_SENSORS,  # Données IMU brutes
    10,  # Fréquence de 10 Hz
    1  # Activer (1) ou désactiver (0)
)

# Activer l'envoi des données de statut étendu
master.mav.request_data_stream_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_EXTENDED_STATUS,
    10,
    1
)

print("📡 Attente des données IMU...")

while True:
    # Récupération des messages MAVLink
    msg = master.recv_match(type=['RAW_IMU', 'SCALED_IMU2', 'SCALED_IMU3', 'ATTITUDE'], blocking=True)

    if msg:
        msg_type = msg.get_type()

        if msg_type in ['RAW_IMU', 'SCALED_IMU2', 'SCALED_IMU3']:
            print(f"📊 {msg_type} - Accélération: x={msg.xacc}, y={msg.yacc}, z={msg.zacc}")
            print(f"🔄 Gyroscope: x={msg.xgyro}, y={msg.ygyro}, z={msg.zgyro}")
            print(f"🧭 Magnétomètre: x={msg.xmag}, y={msg.ymag}, z={msg.zmag}")
        
        elif msg_type == 'ATTITUDE':
            print(f"🎛️ ATTITUDE - Roll={msg.roll:.2f}, Pitch={msg.pitch:.2f}, Yaw={msg.yaw:.2f}")

        print("-" * 50)
