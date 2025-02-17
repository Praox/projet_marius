import socket

# Paramètres du serveur
HOST = '192.168.254.120'  # Remplacez par l'adresse IP de votre serveur
PORT = 3000  # Doit correspondre au port du serveur

# Création du socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connexion au serveur
    client.connect((HOST, PORT))
    
    # Saisie des données à envoyer
    message = input("Entrez le message à envoyer : ")
    
    # Envoi des données au serveur
    client.sendall(message.encode("utf-8"))
    
    print("Message envoyé avec succès !")
    
except ConnectionRefusedError:
    print("Connexion refusée. Vérifiez que le serveur est en cours d'exécution et accessible.")
except Exception as e:
    print(f"Erreur : {e}")
finally:
    # Fermeture de la connexion
    client.close()