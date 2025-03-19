import RPi.GPIO as GPIO
from MCP3008 import MCP3008
from time import sleep

#####################################################################################
###############                    INIT VAR                           ###############
#####################################################################################

# Définition des pins utilisés
ENA_GV = 32  # PWM0 matériel par défaut moteur A GV : GPIO12
sens_GV = 29  # Controle le sens du moteur : GPIO5

ENA_saf = 33  # PWM1 matériel par défaut moteur B Safran : GPIO13
sens_saf = 31  # Controle le sens du moteur : GPIO18 -> GPIO6

# Configuration des GPIOs
GPIO.setmode(GPIO.BOARD)  # Note les entrées avec les numéros des pins et non ceux des GPIOs
GPIO.setup(ENA_GV, GPIO.OUT)  # On utilise le pin 32 comme une sortie GPIO
GPIO.setup(sens_GV, GPIO.OUT)
GPIO.setup(ENA_saf, GPIO.OUT)
GPIO.setup(sens_saf, GPIO.OUT)

# Initialisation des signaux PWM
PWM_GV = GPIO.PWM(ENA_GV, 100)  # Initialise un signal PWM sur une broche GPIO (ENA_GV) à 100 Hz
PWM_saf = GPIO.PWM(ENA_saf, 100)  # Pareil pour le safran
PWM_GV.start(0)  # Le signal vaut 0 (moteur éteint)
PWM_saf.start(0)

# Initialisation du convertisseur ADC MCP3008
adc = MCP3008()

# Définition des angles désirés (en degrés)
desired_angle_GV = 45  # Angle désiré pour la voile (GV)
desired_angle_saf = 30  # Angle désiré pour le safran

# Fonction pour convertir la valeur ADC en angle (en degrés)
def adc_to_angle(adc_value):
    """
    Convertit la valeur ADC (0-1023) en angle (0-180 degrés).
    """
    
    return (adc_value / 1023.0) * 180.0

# Fonction pour contrôler un moteur avec asservissement en position
def control_motor(desired_angle, measured_angle, pwm_pin, sens_pin, pwm_controller):
    """
    Contrôle un moteur avec asservissement en position.
    - desired_angle : Angle désiré (en degrés).
    - measured_angle : Angle mesuré par le potentiomètre (en degrés).
    - pwm_pin : Pin PWM pour contrôler la vitesse du moteur.
    - sens_pin : Pin pour contrôler le sens du moteur.
    - pwm_controller : Objet PWM pour le moteur.
    """
    # Calcul de l'erreur
    error = desired_angle - measured_angle

    # Déterminer le sens de rotation en fonction de l'erreur
    if error > 0:
        GPIO.output(sens_pin, GPIO.HIGH)  # Sens horaire
    else:
        GPIO.output(sens_pin, GPIO.LOW)  # Sens anti-horaire

    # Calcul de la valeur PWM (proportionnelle à l'erreur)
    pwm_value = min(abs(error) * 2, 100)  # Limite la valeur PWM à 100%
    pwm_controller.ChangeDutyCycle(pwm_value)

    # Afficher les informations de débogage
    print(f"Desired: {desired_angle}, Measured: {measured_angle}, Error: {error}, PWM: {pwm_value}")

try:
    while True:
        # Lecture des valeurs des potentiomètres
        value_GV = adc.read(channel=0)  # Lecture du potentiomètre de la voile (GV)
        value_saf = adc.read(channel=1)  # Lecture du potentiomètre du safran

        # Conversion des valeurs ADC en angles (en degrés)
        measured_angle_GV = adc_to_angle(value_GV)
        measured_angle_saf = adc_to_angle(value_saf)

        # Affichage des angles mesurés
        print(f"GV Angle: {measured_angle_GV}, Safran Angle: {measured_angle_saf}")

        # Asservissement de la voile (GV)
        control_motor(desired_angle_GV, measured_angle_GV, ENA_GV, sens_GV, PWM_GV)

        # Asservissement du safran
        control_motor(desired_angle_saf, measured_angle_saf, ENA_saf, sens_saf, PWM_saf)

        # Pause pour éviter de surcharger le CPU
        sleep(0.1)

except KeyboardInterrupt:
    print("Arrêt du programme")
    PWM_GV.stop()
    PWM_saf.stop()
    GPIO.cleanup()