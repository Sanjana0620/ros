# temp_pub

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TempPublisher(Node):
    def __init__(self):
        super().__init__('temperature_publisher')

        self.pub = self.create_publisher(
            Float32,
            '/temperature',
            10
        )

        self.temp = 20.0

        self.create_timer(1.0, self.publish_temp)

        self.get_logger().info('Temperature publisher started.')

    def publish_temp(self):
        msg = Float32()
        msg.data = self.temp

        self.pub.publish(msg)

        self.get_logger().info(
            f'Temp: {self.temp:.1f} C'
        )

        self.temp += 5.0

        if self.temp > 80.0:
            self.temp = 20.0


def main():
    rclpy.init()
    rclpy.spin(TempPublisher())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# humidity_pub

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class HumidityPublisher(Node):
    def __init__(self):
        super().__init__('humidity_publisher')

        self.pub = self.create_publisher(
            Float32,
            '/humidity',
            10
        )

        self.humidity = 40.0

        self.create_timer(1.5, self.publish_humidity)

        self.get_logger().info('Humidity publisher started.')

    def publish_humidity(self):
        msg = Float32()
        msg.data = self.humidity

        self.pub.publish(msg)

        self.get_logger().info(
            f'Humidity: {self.humidity:.1f}%'
        )

        self.humidity += 10.0

        if self.humidity > 90.0:
            self.humidity = 40.0


def main():
    rclpy.init()
    rclpy.spin(HumidityPublisher())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# gas_pub

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class GasPublisher(Node):
    def __init__(self):
        super().__init__('gas_publisher')

        self.pub = self.create_publisher(
            Float32,
            '/gas_level',
            10
        )

        self.gas = 0.0

        self.create_timer(2.0, self.publish_gas)

        self.get_logger().info('Gas publisher started.')

    def publish_gas(self):
        msg = Float32()
        msg.data = self.gas

        self.pub.publish(msg)

        self.get_logger().info(
            f'Gas: {self.gas:.1f} ppm'
        )

        self.gas += 50.0

        if self.gas > 400.0:
            self.gas = 0.0


def main():
    rclpy.init()
    rclpy.spin(GasPublisher())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# safety_monitor

import rclpy

from rclpy.node import Node
from std_msgs.msg import Float32, String

DANGER_TEMP = 60.0
DANGER_GAS = 300.0

WARN_TEMP = 40.0
WARN_HUMID = 80.0
WARN_GAS = 150.0

class SafetyMonitor(Node):
    def __init__(self):
        super().__init__('safety_monitor')

        self.temp = 0.0
        self.humid = 0.0
        self.gas = 0.0

        self.create_subscription(
            Float32,
            '/temperature',
            self.cb_temp,
            10
        )

        self.create_subscription(
            Float32,
            '/humidity',
            self.cb_humid,
            10
        )

        self.create_subscription(
            Float32,
            '/gas_level',
            self.cb_gas,
            10
        )

        self.pub_status = self.create_publisher(
            String,
            '/safety_status',
            10
        )

        self.get_logger().info('Safety Monitor ready.')

    def cb_temp(self, msg):
        self.temp = msg.data
        self._evaluate()

    def cb_humid(self, msg):
        self.humid = msg.data
        self._evaluate()

    def cb_gas(self, msg):
        self.gas = msg.data
        self._evaluate()

    def _evaluate(self):

        if self.temp > DANGER_TEMP or self.gas > DANGER_GAS:

            status = 'DANGER'

            self.get_logger().error(
                f'DANGER | temp={self.temp:.1f}C '
                f'humid={self.humid:.1f}% gas={self.gas:.1f}ppm'
            )

        elif (
            self.temp > WARN_TEMP or
            self.humid > WARN_HUMID or
            self.gas > WARN_GAS
        ):

            status = 'WARNING'

            self.get_logger().warn(
                f'WARNING | temp={self.temp:.1f}C '
                f'humid={self.humid:.1f}% gas={self.gas:.1f}ppm'
            )

        else:

            status = 'SAFE'

            self.get_logger().info(
                f'SAFE | temp={self.temp:.1f}C '
                f'humid={self.humid:.1f}% gas={self.gas:.1f}ppm'
            )

        out = String()
        out.data = status

        self.pub_status.publish(out)


def main():
    rclpy.init()
    rclpy.spin(SafetyMonitor())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
