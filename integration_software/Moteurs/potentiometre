# -*- coding: utf-8 -*-
from MCP3008 import MCP3008
from time import sleep

try:
    while True:
        adc = MCP3008()
        value_GV = adc.read( channel = 0 ) # Vous pouvez bien entendu adapter le canal à lire
        value_SAF = adc.read( channel = 1 )
        print("Tension appliquée GV : %.2f Safran : %.2f" % (value_GV / 1023.0 * 3.3, value_SAF / 1023.0 * 3.3) ) # affichage de la valeur du potentiomètre
        sleep(1) # rafraichissement tout les 1 secondes

except KeyboardInterrupt:
    print("Arrêt du programme")