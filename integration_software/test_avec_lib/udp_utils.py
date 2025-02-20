# udp_utils.py
import socket
import json

BUFFER_SIZE = 1024  # Taille du buffer

def udp_listener(ip, port, callback):
    """
    Écoute les messages UDP entrants sur l'IP et le port spécifiés.
    
    :param ip: Adresse IP d'écoute
    :param port: Port d'écoute
    :param callback: Fonction à appeler avec les données reçues
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    
    print(f"🖥️ Serveur UDP en écoute sur {ip}:{port}")

    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            decoded_data = data.decode('utf-8')  # Convertir en string
            parsed_data = json.loads(decoded_data)  # Convertir en JSON
            
            print(f"📥 Données reçues de {addr}: {parsed_data}")

            # Appeler la fonction callback pour traiter les données
            callback(decoded_data)

        except json.JSONDecodeError:
            print("❌ Erreur : données reçues mal formatées")
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")

def udp_forwarder(data, dest_ip, dest_port):
    """
    Transmet des données en UDP vers un autre appareil.
    
    :param data: Données à envoyer (string)
    :param dest_ip: Adresse IP de destination
    :param dest_port: Port de destination
    """
    try:
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        send_sock.sendto(data.encode('utf-8'), (dest_ip, dest_port))
        print(f"📤 Données envoyées à {dest_ip}:{dest_port}")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi des données : {e}")
