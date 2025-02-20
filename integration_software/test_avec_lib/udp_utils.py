# udp_utils.py
import socket
import json

BUFFER_SIZE = 1024  # Taille du buffer

def udp_listener(ip, port, callback):
    """Écoute les messages UDP entrants et exécute un callback sur les données reçues."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"🖥️ Serveur UDP en écoute sur {ip}:{port}")

    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            decoded_data = data.decode('utf-8')
            parsed_data = json.loads(decoded_data)
            print(f"📥 Données reçues de {addr}: {parsed_data}")
            callback(decoded_data)
        except json.JSONDecodeError:
            print("❌ Erreur : données mal formatées")
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")

def udp_forwarder(data, destinations):
    """
    Envoie des données UDP vers plusieurs destinations.
    
    :param data: Données à envoyer (string ou dictionnaire)
    :param destinations: Liste de tuples (IP, Port)
    """
    try:
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        json_data = data if isinstance(data, str) else json.dumps(data)
        encoded_data = json_data.encode('utf-8')

        for ip, port in destinations:
            send_sock.sendto(encoded_data, (ip, port))
            print(f"📤 Données envoyées à {ip}:{port}")

    except Exception as e:
        print(f"❌ Erreur lors de l'envoi des données : {e}")
