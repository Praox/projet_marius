import tools_nav
import numpy as np

def navigation(tack_points, wind_angle, wind_speed, position_GPS, taille_maille, rayon_tolerance):

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

    estimated_speed = tools_nav.nds_speed2_ms_speed(tools_nav.get_speed(wind_speed, cap_vent_relatif))
    

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
