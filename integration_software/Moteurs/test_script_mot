# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep

# Définition des pins utilisés
ENA_GV = 33  # PWM0 matériel par défaut moteur A GV : GPIO12
sens_GV = 31  # Controle le sens du moteur : GPIO5

# Configuration des GPIOs
GPIO.setmode(GPIO.BOARD) # note les entrées avec les numéros des pins et non ceux des GPIOs
GPIO.setup(ENA_GV, GPIO.OUT) # on utilise le pin 32 comme une sortie GPIO
GPIO.setup(sens_GV, GPIO.OUT)

# Initialisation des signaux PWM
PWM_GV = GPIO.PWM(ENA_GV, 100) # initialise un signal PWM sur une broche GPIO (ENA_GV) à 100 Hz
PWM_GV.start(0) # le signal vaut 0 (moteur éteint)

try:
    while True:
        # Test moteur 1 (GV) :
        GPIO.output(sens_GV, GPIO.LOW) # on force le sens de rotation du moteur
        # HIGH = tension négative aux bornes du moteur (LED verte) -> rotation sens anti-horaire vu de dessus -> voile à babord
        PWM_GV.ChangeDutyCycle(20) # on fait tourner le moteur à 30% de sa vitesse

        sleep(1) # maintient la vitesse pendant 5 secondes

        PWM_GV.ChangeDutyCycle(0)

        sleep(2) # s'arrête pendant 2s

        GPIO.output(sens_GV, GPIO.LOW) # on inverse le sens de rotation du moteur
        # LOW = tension positive aux bornes du moteur (LED rouge) -> rotation sens horaire vu de dessus -> voile à tribord
        PWM_GV.ChangeDutyCycle(20)

        sleep(1) # les moteurs tournent dans l'autre sens pendant 5s

        PWM_GV.ChangeDutyCycle(0)

        sleep(2) # s'arrête pendant 2s

except KeyboardInterrupt:
    print("Arrêt du programme")
    PWM_GV.stop()
    GPIO.cleanup()