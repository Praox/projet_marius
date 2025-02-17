import socket
import threading

### Initialisation du serveur

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(('192.168.254.120',3000)) #Ecoute sur le port 3000
serveur.listen()

while True :
    client, infosclient = serveur.accept()
    request = client.recv(1024)
    print(request.decode("utf-8")) #affiche les données du client
    print(f"IP client connecté: {infosclient[0]}")  # Affiche l'adresse IP réelle du client
    client.close()

serveur.close()