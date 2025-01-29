import smbus
import DFRobot_BMX160
import time
import socket
import json

class BMX160_sensor_TCA9548A:
    def __init__(self, config_sensor, bus_number):
        self.channel = config_sensor["channel"]
        self.sensor = DFRobot_BMX160.BMX160(bus=bus_number, addr=config_sensor["address"])
        self.data = []
        while not self.sensor.begin():
            time.sleep(1)

class TCA9548A:
    def __init__(self, config_sensor=None, bus_number=6, address=0x70):
        """
        Initialise une instance pour communiquer avec le TCA9548A sur un bus spécifique.

        :param bus_number: Numéro du bus I2C (par défaut : 6).
        :param address: Adresse I2C du TCA9548A (par défaut : 0x70).
        """
        self.bus = smbus.SMBus(bus_number)  # Initialiser le bus I2C
        self.address = address               # Adresse du multiplexeur TCA9548A
        self.sensors = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = "192.168.254.15"
        self.port = 14555
        self.t0 = None
        config_sensor = [] if config_sensor is None else config_sensor
        for cf in config_sensor:
            self.select_channel(cf["channel"])
            self.sensors.append(BMX160_sensor_TCA9548A(config_sensor=cf, bus_number=bus_number))

    def select_channel(self, channel):
        """
        Sélectionne un canal spécifique sur le TCA9548A.

        :param channel: Numéro du canal à activer (0 à 7).
        """
        if not 0 <= channel <= 7:
            raise ValueError("Le canal doit être compris entre 0 et 7")

        # Écrire dans le registre du multiplexeur pour activer le canal
        self.bus.write_byte(self.address, 1 << channel)

    def scan_sensor(self, sensor_number):
        """
        Scanne les périphériques sur un canal spécifique.

        :param channel: Numéro du canal à scanner (0 à 7).
        :return: Liste des adresses des périphériques trouvés.
        """
        sensor = self.sensors[sensor_number]
        channel, address = sensor.channel, sensor.sensor.i2c_addr
        self.select_channel(channel)  # Activer le canal
        devices = []
        self.bus.write_quick(address)
        devices.append(hex(address))
        return devices

    def scan_all_sensors(self):
        """
        Scanne tous les canaux du TCA9548A.

        :return: Dictionnaire avec les canaux comme clés et les adresses des périphériques trouvés comme valeurs.
        """
        results = []
        for i in range(len(self.sensors)):
            results.append(self.scan_sensor(i))
        return results

    def read_sensor(self, sensor_number, send_udp=True):
        """
        Lis les valeurs du sensor
        """
        sensor = self.sensors[sensor_number]
        channel, address = sensor.channel, sensor.sensor.i2c_addr
        self.select_channel(channel)
        ti = time.time() - self.t0
        data = sensor.sensor.get_all_data()
        data_dict = {
            "sensor": sensor_number, "t": ti, "magx": data[0], "magy": data[1], "magz": data[2], "gyrx": data[3], "gyry": data[4], "gyrz": data[5], "accx": data[6], "accy": data[7], "accz": data[8]
        }
        if send_udp:
            self.send_data_udp(data_dict)
            print("udp data sent for sensor ", sensor_number)
        else:
            sensor.data.append(data_dict)
            # print("sensor ", sensor_number, " : ")
            print("sensor ", sensor_number, ", ti : ", ti)
            # for key, val in data_dict.items():
            #    print(key, val)

    def send_data_udp(self, data_dict):
        message = json.dumps(data_dict)
        self.socket.sendto(message.encode('utf-8'), (self.host, self.port))

    def read_all_sensors(self, f=2, T=5):
        if self.t0 is None:
            self.t0 = time.time()
        dt = 1/f
        next_t = dt
        while time.time()-self.t0 < T:
            for i in range(len(self.sensors)):
                self.read_sensor(i)
            while time.time()-self.t0 < next_t:
                pass
            next_t += dt

    def print_all_data(self):
        sensor = self.sensors[0]
        for d in sensor.data:
            print(d)

# Exemple d'utilisation
if __name__ == "__main__":
    config_sensor = [
        {"channel": 0, "address": 0x68},
        {"channel": 2, "address": 0x69},
        {"channel": 6, "address": 0x68}
    ]
    time.sleep(1)
    # Spécifiez le numéro de bus I2C
    tca = TCA9548A(config_sensor=config_sensor, bus_number=6)
    # Scanne tous les canaux
    all_devices = tca.scan_all_sensors()
    print("all_devices : ", all_devices)
    f = 30
    T = 3600*5
    tca.read_all_sensors(f=f, T=T)
    tca.print_all_data()