import heapq
import numpy as np
import matplotlib.pyplot as plt

# Tableau de vitesses (extrait du diagramme de polarité)
polar_table = {
    5: {0: 0, 45: 2, 60: 3, 75: 3.5, 90: 3, 105: 2.5, 120: 2, 135: 1.5, 150: 1, 180: 0},
    10: {0: 0, 45: 4, 60: 5, 75: 5.5, 90: 5, 105: 4.5, 120: 4, 135: 3, 150: 2, 180: 0},
    15: {0: 0, 45: 6, 60: 7, 75: 7.5, 90: 7, 105: 6.5, 120: 5.5, 135: 4, 150: 3, 180: 0},
    20: {0: 0, 45: 7, 60: 8, 75: 8.5, 90: 8, 105: 7.5, 120: 6.5, 135: 5, 150: 4, 180: 0},
}

def heuristic(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def nds_speed2_ms_speed(nds_speed):
    return 0.514444 * nds_speed

def get_speed(wind_speed, angle):
    available_speeds = sorted(polar_table.keys())
    if wind_speed in polar_table:
        angle_keys = sorted(polar_table[wind_speed].keys())
        if angle in polar_table[wind_speed]:
            return polar_table[wind_speed][angle]
        lower_angle = max([a for a in angle_keys if a <= angle], default=angle_keys[0])
        upper_angle = min([a for a in angle_keys if a >= angle], default=angle_keys[-1])
        if lower_angle == upper_angle:
            return polar_table[wind_speed][lower_angle]
        speed_low = polar_table[wind_speed][lower_angle]
        speed_high = polar_table[wind_speed][upper_angle]
        interpolated_speed = speed_low + (speed_high - speed_low) * (angle - lower_angle) / (upper_angle - lower_angle)
        return interpolated_speed

    lower = max([ws for ws in available_speeds if ws <= wind_speed], default=available_speeds[0])
    upper = min([ws for ws in available_speeds if ws >= wind_speed], default=available_speeds[-1])
    if lower == upper:
        return get_speed(lower, angle)

    speed_lower = get_speed(lower, angle)
    speed_upper = get_speed(upper, angle)
    return speed_lower + (speed_upper - speed_lower) * (wind_speed - lower) / (upper - lower)

def compute_penalty(grid, radius=5, penalty_value=2, obstacle_penalty=10):
    penalty_grid = np.zeros_like(grid, dtype=float)
    obstacle_positions = np.argwhere(grid == 1)
    for ox, oy in obstacle_positions:
        penalty_grid[ox, oy] = obstacle_penalty  # Augmente la pénalité des obstacles
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx, ny = ox + dx, oy + dy
                if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] == 0:
                    penalty_grid[nx, ny] += penalty_value / (abs(dx) + abs(dy) + 1)
    return penalty_grid

def get_neighbors(node, wind_angle, wind_speed, grid, penalty_grid, previous_angle=None):
    x, y = node # Position actuelle
    neighbors = [] # Liste des voisins
    step = 1  # Distance d'un déplacement
    cout_virement = 10
    allowed_angles = [45, -45, 60, -60, 75, -75, 90, 105, -105, 120, -120, 135, -135] # Angles autorisés pour le voilier
    for angle in allowed_angles: # Parcours tous les angles possibles
        direction = np.radians(wind_angle + angle) # Convertit l'angle en radians
        dx = int(np.round(step * np.cos(direction))) # Déplacement en x
        dy = int(np.round(step * np.sin(direction))) # Déplacement en y
        neighbor = (x + dx, y + dy)  # Détermine la position du voisin
        if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1]: # Vérifie les limites de la grille
            if grid[neighbor] == 0: # Vérifie si la case est navigable
                speed = get_speed(wind_speed, abs(angle)) # Obtient la vitesse en fonction de l'angle
                if speed > 0: # Vérifie que le voilier peut avancer
                    change_cost = 0 if previous_angle is None or abs(previous_angle - angle) <= 45 else cout_virement # Coût de changement de direction
                    penalty = penalty_grid[neighbor] # Récupère la pénalité de la case
                    neighbors.append((neighbor, 1 / speed + change_cost + penalty, angle)) # Ajoute le voisin à la liste
    return neighbors # Retourne la liste des voisins

def a_star(start, goal, wind_angle, wind_speed, grid):
    penalty_grid = compute_penalty(grid) # Génère la grille de pénalité
    open_set = [] # Liste des nœuds à explorer
    heapq.heappush(open_set, (0, start, None)) # Ajoute le point de départ avec une priorité nulle
    came_from = {}  # Stocke le chemin
    g_score = {start: 0} # Coût du chemin de départ
    f_score = {start: heuristic(start, goal)} # Coût estimé total
    angle_from = {} # Angle de navigation

    while open_set:  # Tant que la liste des nœuds à explorer n'est pas vide
        _, current, current_angle = heapq.heappop(open_set) # Récupère le nœud avec le coût le plus bas
        if current == goal: # Si l'on atteint l'objectif
            path = [] # Initialisation du chemin
            tack_points = [] # Points de virement
            prev_angle = None # Dernier angle utilisé
            while current in came_from: # Reconstruction du chemin
                if prev_angle is not None and angle_from[current] != prev_angle:
                    tack_points.append((current, angle_from[current]))
                path.append(current)
                prev_angle = angle_from[current]
                current = came_from[current]
            path.append(start)
            return path[::-1], tack_points[::-1], penalty_grid

        for neighbor, move_cost, angle in get_neighbors(current, wind_angle, wind_speed, grid, penalty_grid, current_angle):
            tentative_g_score = g_score[current] + move_cost
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                angle_from[neighbor] = angle
                heapq.heappush(open_set, (f_score[neighbor], neighbor, angle))
    return None, None, penalty_grid

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


# Paramètres de simulation
waypoints = [(125, 130), (100, 25), (25, 100), (125, 130)]
wind_angle = int(input("Entrez l'angle du vent en degrés: "))
wind_speed = int(input("Entrez la vitesse du vent en noeuds: "))
taille_maille = 50 # en m
rayon_tolerance = 100 / taille_maille
position_GPS = (67, 72)


def compute_full_path(waypoints, wind_angle, wind_speed, grid):
  total_path = []
  total_tack_points = []
  for i in range(len(waypoints) - 1):
    start, goal = waypoints[i], waypoints[i + 1]
    path, tack_points, penalty_grid = a_star(start, goal, wind_angle, wind_speed, grid)
    if path:
        total_path.extend(path[:-1])  # Évite les doublons
        total_tack_points.extend(tack_points)
  total_path.append(waypoints[-1])
  return total_path, total_tack_points, penalty_grid

total_path, tack_points, penalty_grid = compute_full_path(waypoints, wind_angle, wind_speed, grid)

# Fonction d'affichage des zone de tolérance des waypoints
def draw_tolerance_circle(point, rayon_tolerance, color='r', linestyle='dashed'):
    """
    Ajoute un cercle de tolérance autour d'un point donné sur un graphique existant.
    """
    cercle = plt.Circle((point[1], point[0]), rayon_tolerance, color=color, fill=False, linestyle=linestyle)
    plt.gca().add_patch(cercle)



# Affichage du résultat
print(tack_points)
plt.figure(figsize=(10, 10))





def navigation(next_waypoint, wind_angle, wind_speed, position_GPS, taille_maille, rayon_tolerance):

    if not tack_points:  # Vérifie s'il reste des waypoints
        print("Tous les waypoints ont été validés.")
        return

    next_waypoint = tack_points[0]
    
    print(f"Prochain waypoint : {next_waypoint[0]}")

    ## Calcul de la distance au prochain Waypoint
    delta_x = next_waypoint[0][0] - position_GPS[0]
    delta_y = next_waypoint[0][1] - position_GPS[1]
    distance = np.sqrt(delta_x**2 + delta_y**2) * taille_maille  # Conversion en mètres

    print(f"Distance jusqu'au virement : {distance} m")

    ## Validation d'un waypoint
    if distance < rayon_tolerance:
        print("Validation du waypoint")
        tack_points.pop(0)  # Supprime le premier élément

        if tack_points:  # Vérifie s'il reste des waypoints
            print("Recalcul de la navigation vers le prochain waypoint...")
            return navigation(tack_points, wind_angle, wind_speed, position_GPS, taille_maille, rayon_tolerance)
        else:
            print("Tous les waypoints ont été atteints.")
        return 

    ## Verification que le cap est dans les polaires du bateau
    cap_boussole = np.degrees(np.arctan2(delta_y, delta_x))
    print(f"Cap boussole avant correction : {cap_boussole}")
    cap_vent_relatif = (cap_boussole - wind_angle) % 360
    cap_vent_relatif = 360 - cap_vent_relatif if cap_vent_relatif > 180 else cap_vent_relatif

    print(f"Cap vent relatif avant vérification polaire : {cap_vent_relatif}")

    # Convertir en cap boussole corrigé
    if cap_vent_relatif > 180:
        cap_vent_relatif -= 360

    if 0 < cap_vent_relatif < 45:
        cap_stock = cap_vent_relatif
        cap_vent_relatif = 45
        cap_boussole_corrige = cap_boussole + cap_stock-cap_vent_relatif
        print(f"Cap boussole après correction : {cap_boussole_corrige}")
    elif -45 < cap_vent_relatif < 0:
        cap_stock = cap_vent_relatif
        cap_vent_relatif = -45
        cap_boussole_corrige = cap_boussole + cap_stock-cap_vent_relatif
        print(f"Cap boussole après correction : {cap_boussole_corrige}")
    else:
        cap_boussole_corrige = cap_boussole
        print(f"Cap boussole après correction : {cap_boussole_corrige}")

    estimated_speed = nds_speed2_ms_speed(get_speed(wind_speed, cap_vent_relatif))
    

    print(f"Vitesse estimée : {estimated_speed} m/s")

    estimated_time = distance / estimated_speed if estimated_speed > 0 else float('inf')

    print(f"Temps estimé : {estimated_time} secondes")

    print(f"Cap vent relatif : {cap_vent_relatif}")

    # Calcul du vecteur vitesse
    cap_boussole_rad = np.radians(cap_boussole_corrige)  # Conversion en radians
    Vx = estimated_speed * np.cos(cap_boussole_rad)
    Vy = estimated_speed * np.sin(cap_boussole_rad)

    print(f"Vecteur vitesse : ({Vx}, {Vy}) m/s")

    return cap_boussole_corrige, cap_vent_relatif, estimated_time, estimated_speed, distance, (Vx, Vy) 


cap___ = navigation(tack_points[0], wind_angle, wind_speed, position_GPS, taille_maille, rayon_tolerance)
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
