import socket
import threading

# Adresse IP de l'antenne réceptrice et le port
#RECEIVER_IP = "127.0.0.1"
RECEIVER_IP = "192.168.254.115"   # Remplacez par l'IP de l'antenne réceptrice
RECEIVER_PORT = 14555
ADDR = (RECEIVER_IP,RECEIVER_PORT)

# Création du socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Émetteur UDP prêt à envoyer des messages.")
try:
    while True:
        message = "test"
        sock.sendto(message.encode('utf_8'), ADDR)
        print("Message envoyé !")

except KeyboardInterrupt:
    print("\nArrêt de l'émetteur.")
finally:
    sock.close()
