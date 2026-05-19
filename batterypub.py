# battery_pub

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class BatteryPublisher(Node):
    def __init__(self):
        super().__init__('battery_publisher')

        self.pub = self.create_publisher(
            Float32,
            '/battery_level',
            10
        )

        self.battery = 100.0

        self.create_timer(1.0, self.publish_battery)

        self.get_logger().info('Battery publisher started.')

    def publish_battery(self):
        msg = Float32()
        msg.data = self.battery

        self.pub.publish(msg)

        self.get_logger().info(
            f'Battery: {self.battery:.1f}%'
        )

        self.battery -= 5.0

        if self.battery < 0.0:
            self.battery = 100.0


def main():
    rclpy.init()
    rclpy.spin(BatteryPublisher())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# speed_pub

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class SpeedPublisher(Node):
    def __init__(self):
        super().__init__('speed_publisher')

        self.pub = self.create_publisher(
            Float32,
            '/robot_speed',
            10
        )

        self.speed = 2.0

        self.create_timer(1.0, self.publish_speed)

        self.get_logger().info('Speed publisher started.')

    def publish_speed(self):
        msg = Float32()
        msg.data = self.speed

        self.pub.publish(msg)

        self.get_logger().info(
            f'Desired speed: {self.speed:.2f} m/s'
        )


def main():
    rclpy.init()
    rclpy.spin(SpeedPublisher())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# battery_monitor

import rclpy

from rclpy.node import Node
from std_msgs.msg import Float32

LOW_BATTERY = 20.0

class BatteryMonitor(Node):
    def __init__(self):
        super().__init__('battery_monitor')

        self.battery = 100.0
        self.speed = 0.0

        self.create_subscription(
            Float32,
            '/battery_level',
            self.cb_battery,
            10
        )

        self.create_subscription(
            Float32,
            '/robot_speed',
            self.cb_speed,
            10
        )

        self.pub_safe = self.create_publisher(
            Float32,
            '/safe_speed',
            10
        )

        self.get_logger().info('Battery Monitor ready.')

    def cb_battery(self, msg):
        self.battery = msg.data
        self._decide()

    def cb_speed(self, msg):
        self.speed = msg.data
        self._decide()

    def _decide(self):
        if self.battery < LOW_BATTERY:
            safe = self.speed / 2.0

            self.get_logger().warn(
                f'LOW BATTERY ({self.battery:.1f}%) '
                f'| {self.speed:.2f} -> {safe:.2f} m/s'
            )

        else:
            safe = self.speed

            self.get_logger().info(
                f'Battery OK ({self.battery:.1f}%) '
                f'| Speed: {safe:.2f} m/s'
            )

        out = Float32()
        out.data = safe

        self.pub_safe.publish(out)


def main():
    rclpy.init()
    rclpy.spin(BatteryMonitor())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
