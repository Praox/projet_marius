import socket
import threading

# Adresse de l'antenne réceptrice UDP
RECEIVER_IP = "192.168.254.115"   
RECEIVER_PORT = 14555
ADDR = (RECEIVER_IP, RECEIVER_PORT)

# Adresse du serveur TCP
TCP_IP = "192.168.254.120"
TCP_PORT = 3000

# Flag d'arrêt
stop_flag = False

# Fonction d'envoi UDP
def udp_sender():
    global stop_flag
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Émetteur UDP prêt à envoyer des messages.")

    while not stop_flag:
        message = input("Entrez un message à envoyer : ")
        sock.sendto(message.encode('utf-8'), ADDR)
        print("Message envoyé !")

    sock.close()
    print("Transmission UDP arrêtée.")

# Fonction de réception TCP
def tcp_listener():
    global stop_flag
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind((TCP_IP, TCP_PORT))  
    serveur.listen()

    print(f"Serveur TCP en écoute sur {TCP_IP}:{TCP_PORT}...")

    client, infosclient = serveur.accept()
    request = client.recv(1024)
    
    if request:
        print(f"Message TCP reçu : {request.decode('utf-8')}")
        print(f"IP client connecté : {infosclient[0]}")
        stop_flag = True  # Active le flag d'arrêt

    client.close()
    serveur.close()
    print("Serveur TCP fermé.")

# Lancer les threads
udp_thread = threading.Thread(target=udp_sender)
tcp_thread = threading.Thread(target=tcp_listener)

udp_thread.start()
tcp_thread.start()

# Attendre la fin des threads
udp_thread.join()
tcp_thread.join()

print("Programme terminé.")
