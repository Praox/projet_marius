import tools_nav
import heapq
import numpy as np

def heuristic(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

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
                speed = tools_nav.get_speed(wind_speed, abs(angle)) # Obtient la vitesse en fonction de l'angle
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

