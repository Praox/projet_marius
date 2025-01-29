import socket

# Adresse IP de l'antenne réceptrice et le port
RECEIVER_IP = "192.168.254.102"  # Remplacez par l'IP de l'antenne réceptrice
RECEIVER_PORT = 14555

# Création du socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Émetteur UDP prêt à envoyer des messages.")
try:
    while True:
        message = input("Entrez un message à envoyer : ")
        sock.sendto(message.encode(), (RECEIVER_IP, RECEIVER_PORT))
        print("Message envoyé !")

except KeyboardInterrupt:
    print("\nArrêt de l'émetteur.")
finally:
    sock.close()
