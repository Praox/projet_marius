import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class NMEAListener(Node):
    def __init__(self):
        super().__init__('nmea_listener')
        
        # Création du subscriber sur le topic /nmea
        self.subscription = self.create_subscription(
            String,
            'nmea',
            self.listener_callback,
            10)
        self.subscription  # Pour éviter l'optimisation du garbage collector

        self.get_logger().info('NMEA Listener prêt à écouter...')

    def listener_callback(self, msg):
        """Callback exécuté lorsqu'un message est reçu sur /nmea"""
        self.get_logger().info(f'Trame reçue : {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = NMEAListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Arrêt du listener.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
