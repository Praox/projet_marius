import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
from pynmeagps import NMEAReader

class NMEASerialPublisher(Node):
    def __init__(self):
        super().__init__('nmea_serial_publisher')
        
        # Déclaration des paramètres (modifiable via la ligne de commande)
        self.declare_parameter('port', '/dev/ttyUSB0')  # COM4 sous Windows
        self.declare_parameter('baudrate', 4800)
        
        port = self.get_parameter('port').get_parameter_value().string_value
        baudrate = self.get_parameter('baudrate').get_parameter_value().integer_value

        # Création du publisher sur le topic /nmea
        self.publisher_ = self.create_publisher(String, 'nmea', 10)
        self.get_logger().info(f'Lecture série {port} à {baudrate} baud')

        try:
            self.serial_port = serial.Serial(port, baudrate, timeout=1)
            self.nmea_reader = NMEAReader(self.serial_port)
            self.timer = self.create_timer(0.1, self.read_serial_data)  # 10 Hz
        except serial.SerialException as e:
            self.get_logger().error(f"Erreur port série : {e}")
    
    def read_serial_data(self):
        """Lit les données NMEA et les publie sur le topic"""
        try:
            (raw_data, _) = self.nmea_reader.read()
            if raw_data:
                msg = String()
                msg.data = raw_data.decode('utf-8').strip()
                self.publisher_.publish(msg)
                self.get_logger().info(f'Trame envoyée : {msg.data}')
        except Exception as e:
            self.get_logger().error(f'Erreur de lecture : {e}')

def main(args=None):
    rclpy.init(args=args)
    node = NMEASerialPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Arrêt du publisher.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
