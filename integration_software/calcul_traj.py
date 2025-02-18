import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 4000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"🖥️ Serveur UDP en écoute sur {UDP_IP}:{UDP_PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    print(f"📥 Données reçues de {addr} : {data.decode('utf-8')}")
