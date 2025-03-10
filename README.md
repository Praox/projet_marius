# Project Autonomus Sailboat : Marius
## autonomous sailboat
Dans ce git vous trouverez tous les protocoles de commication pour les différents réseaux (local et privé). Ainsi que les tentatives d'implémentation d'un alogrithme de détermination de trajectoire.


### Comment ça marche pour le moment?
Nous avons decidé de structurer le code en plusieur scripts python distincts qui communiquent entre eux via un réseaux local. 
- Le premier script: read_N_decrypt.py (/integration_software/avec_lib....) permet la lecture et la mise en forme de toutes les données capteurs (AIRMAR, Pixhawk...). Il fait appelle a une bibliothèque sur mesure pour envoyer dans un second temps les données sur le réseau en UDP.
- Le deuxième script : calcul_traj.py effectue lui le calucl de la trajectoire, il est encore en cours de réalisation mais peut se décomposer en 3 parties, la planification, la navigation et enfin la commande moteur. Il envoie lui aussi des données sur le réseau local. (Chaque partie est décomposée en fichier discint puis est appelée dans un script main).
- Le troisième script : send_to_network.py lui recolte toutes les données sur le réseau local et les envoie sur le réseau privé sans fils pour la communication avec l'ordinateur.
- Le quatrième script : IHM_ordi.py troune sur l'ordinateur, il affiche les données reçu sans fils.
- Le cinquième script : client_tcp.py (/udp_test_protocole..) sert lui à envoyé des data et prochainement des commande en TCP au script de calcul de trajectoire.


IMPORTANT:
IP fixe de l'ordinateur doit être : 192.168.254.15
Il faut aussi autorisé la communication en UDP sur le port 14555
La PI elle a pour IP fixe 192.168.254.120
L'antenne de la PI : 192.168.254.101
L'antenne de l'ordi : 192.168.254.102

