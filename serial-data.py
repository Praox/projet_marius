import serial
from pynmeagps import NMEAReader

# Remplacez 'COM1' par le port série réel de votre ordinateur
#with serial.Serial('COM6', 4800, timeout=3) as stream:
#    nmr = NMEAReader(stream)

## while True:
        # Lire une trame NMEA brute
        #raw_data = stream.readline().decode('ascii', errors='ignore')
        
        # Si une trame valide a été lue
        #if raw_data:
        #    parsed_data = nmr.parse(raw_data)
        #    if parsed_data is not None:
        #        print(parsed_data)


##CODE Lecture direct serial OK !!!
#import serial

#try:
#    with serial.Serial('COM4', 4800, timeout=10) as stream:
#        raw_data = stream.read(400)  # Lire 100 octets
#        print('Serial')
#        print(raw_data)
#except serial.SerialException as e:
#    print(f"Erreur de port série : {e}")
#except FileNotFoundError:
#    print("Le port spécifié n'existe pas ou n'est pas accessible.")

import serial

def parse_nmea(data):
    """Traite et identifie les trames NMEA."""
    lines = data.split('\r\n')  # Découper les données en lignes
    valid_frames = []

    for line in lines:
        if line.startswith('$'):  # Vérifie que c'est une trame NMEA
            if validate_checksum(line):
                frame_type = line[1:6]  # Identifie le type (par ex. GPVTG, GPGGA)
                valid_frames.append((frame_type, line))
            else:
                print(f"Trame invalide (checksum incorrect) : {line}")

    return valid_frames


def validate_checksum(nmea_line):
    """Valide la trame NMEA en comparant le checksum."""
    try:
        # Trouver la position du '*'
        star_idx = nmea_line.index('*')
        transmitted_checksum = nmea_line[star_idx + 1:]  # Après le '*'
        data_to_check = nmea_line[1:star_idx]  # Entre '$' et '*'

        # Calculer le checksum XOR
        calculated_checksum = 0
        for char in data_to_check:
            calculated_checksum ^= ord(char)

        # Comparer le checksum calculé avec celui transmis
        return f"{calculated_checksum:02X}" == transmitted_checksum.upper()
    except ValueError:
        # Si le '*' est absent, la trame est invalide
        return False


def read_serial(port, baudrate):
    """Lit les données en temps réel depuis le port série."""
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print(f"Lecture des données série sur {port} (Ctrl+C pour arrêter)")
            buffer = ""

            while True:
                raw_data = ser.read(100)  # Lire 100 octets à la fois
                buffer += raw_data.decode('utf-8', errors='ignore')  # Ajouter au tampon

                # Vérifier s'il y a des trames complètes dans le tampon
                if '\r\n' in buffer:
                    lines = buffer.split('\r\n')
                    buffer = lines[-1]  # Garder la partie incomplète pour la prochaine itération
                    for line in lines[:-1]:
                        frames = parse_nmea(line)
                        for frame_type, frame in frames:
                            print(f"Type: {frame_type}, Trame: {frame}")

    except serial.SerialException as e:
        print(f"Erreur de port série : {e}")
    except KeyboardInterrupt:
        print("\nArrêt de la lecture série.")

# Configuration du port série
PORT = 'COM4'  # Remplacez par le port série utilisé (par exemple, COM4, /dev/ttyUSB0)
BAUDRATE = 4800  # Assurez-vous que cela correspond au périphérique

# Démarrage de la lecture série
read_serial(PORT, BAUDRATE)



