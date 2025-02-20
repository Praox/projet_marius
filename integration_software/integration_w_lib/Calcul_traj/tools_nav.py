# Tableau de vitesses (extrait du diagramme de polarité)
polar_table = {
    5: {0: 0, 45: 2, 60: 3, 75: 3.5, 90: 3, 105: 2.5, 120: 2, 135: 1.5, 150: 1, 180: 0},
    10: {0: 0, 45: 4, 60: 5, 75: 5.5, 90: 5, 105: 4.5, 120: 4, 135: 3, 150: 2, 180: 0},
    15: {0: 0, 45: 6, 60: 7, 75: 7.5, 90: 7, 105: 6.5, 120: 5.5, 135: 4, 150: 3, 180: 0},
    20: {0: 0, 45: 7, 60: 8, 75: 8.5, 90: 8, 105: 7.5, 120: 6.5, 135: 5, 150: 4, 180: 0},
}

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

