import cmd
import navigation
import planification
import numpy as np
import matplotlib.pyplot as plt

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

# Fonction d'affichage des zone de tolérance des waypoints
def draw_tolerance_circle(point, rayon_tolerance, color='r', linestyle='dashed'):
    """
    Ajoute un cercle de tolérance autour d'un point donné sur un graphique existant.
    """
    cercle = plt.Circle((point[1], point[0]), rayon_tolerance, color=color, fill=False, linestyle=linestyle)
    plt.gca().add_patch(cercle)


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


def main():
  return None

plt.title(f"Simulation - Vent {wind_angle}° à {wind_speed} nds")
plt.legend()
plt.grid()
plt.show()