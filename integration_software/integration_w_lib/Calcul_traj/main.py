import cmd
import navigation
import planification
import numpy as np
import time
import tools
#import matplotlib.pyplot as plt
import threading
import json

# Initialisation de la grille
grid = np.zeros((200, 200))

# Ajout d'obstacles
for j in range(50, 75):
    grid[j, 125] = 1
for j in range(0, 25):
    grid[75+j, 125+j] = 1
for j in range(100, 125):
    grid[j, 150] = 1
for j in range(0, 25):
    grid[50-j, 125+j] = 1
for j in range(0, 25):
    grid[125+j, 150-j] = 1
for j in range(75, 125):
    grid[150, j] = 1

''''
# Fonction d'affichage des zone de tolérance des waypoints
def draw_tolerance_circle(point, rayon_tolerance, color='r', linestyle='dashed'):
    """
    Ajoute un cercle de tolérance autour d'un point donné sur un graphique existant.
    """
    cercle = plt.Circle((point[1], point[0]), rayon_tolerance, color=color, fill=False, linestyle=linestyle)
    plt.gca().add_patch(cercle)
'''


# Paramètres de simulation
waypoints = [(125, 130), (100, 25), (25, 100), (125, 130)]
wind_angle = int(input("Entrez l'angle du vent en degrés: "))
wind_speed = int(input("Entrez la vitesse du vent en noeuds: "))
taille_maille = 50 # en m
rayon_tolerance = 100 / taille_maille
position_GPS = (67, 72)


total_path, tack_points, penalty_grid = planification.compute_full_path(waypoints, wind_angle, wind_speed, grid)

cap___ = navigation.navigation(tack_points, wind_angle, wind_speed, position_GPS, taille_maille, rayon_tolerance)
(Vx, Vy) = cap___[5]

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
        #latest_data = tools.json.loads(data)  # Assure-toi que 'data' est bien un JSON
        # Création d'un dictionnaire structuré
        data = {
            "tack_points": tack_points,  # Liste de tuples ((x, y), angle)
            "cap_boussole_corrige": cap___[0],
            "cap_vent_relatif": cap___[1],
            "estimated_time": cap___[2],
            "estimated_speed": cap___[3],
            "distance": cap___[4],
            "vecteur_vitesse": cap___[5]  # Tuple (Vx, Vy)
            }
        #cap = [total_path, tack_points, penalty_grid, cap___]
        if data is not None:  
            tools.udp_forwarder(data, UDP_DESTINATIONS)
    except json.JSONDecodeError:
        print("❌ Erreur : données reçues mal formatées")


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


''''
plt.imshow(penalty_grid, cmap='gray_r', origin='lower')
if total_path:
    path_x, path_y = zip(*total_path)
    plt.plot(path_y, path_x, color='b', label='Trajectoire')
for point, angle in tack_points:
    plt.scatter(point[1], point[0], color='purple', marker='x', label=f'Virement {angle}°')
    draw_tolerance_circle(point, rayon_tolerance)
for i, point in enumerate(waypoints):
    if i == 0:
        plt.scatter(point[1], point[0], color='green', marker='o', label='Départ')
    elif i == len(waypoints) - 1:
        plt.scatter(point[1], point[0], color='blue', marker='o', label='Arrivée')
        #draw_tolerance_circle(point, rayon_tolerance)
    else:
        plt.scatter(point[1], point[0], color='red', marker='o', label='Waypoints')
        draw_tolerance_circle(point, rayon_tolerance)
plt.scatter(position_GPS[1], position_GPS[0], color='orange', marker='*', label='Position GPS')
plt.quiver(100, 175, -np.sin(np.radians(wind_angle))*10, -np.cos(np.radians(wind_angle))*10, angles='xy', scale_units='xy', scale=1, color='blue', label='Vecteur vent')
plt.quiver(position_GPS[1], position_GPS[0], Vy*10, Vx*10, angles='xy', scale_units='xy', scale=1, color='red', label='Vecteur vitesse')


plt.title(f"Simulation - Vent {wind_angle}° à {wind_speed} nds")
plt.legend()
plt.grid()
plt.show()
'''