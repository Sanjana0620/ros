# robot1_pub

import rclpy
import math

from rclpy.node import Node
from std_msgs.msg import String

class Robot1Publisher(Node):
    def __init__(self):
        super().__init__('robot1_publisher')

        self.pub = self.create_publisher(
            String,
            '/robot1_position',
            10
        )

        self.t = 0.0

        self.create_timer(0.5, self.publish_pos)

        self.get_logger().info('Robot 1 publisher started.')

    def publish_pos(self):
        x = 3.0 * math.cos(self.t)
        y = 3.0 * math.sin(self.t)

        self.t += 0.2

        msg = String()
        msg.data = f'{x:.2f},{y:.2f}'

        self.pub.publish(msg)

        self.get_logger().info(
            f'Robot1: ({x:.2f}, {y:.2f})'
        )


def main():
    rclpy.init()
    rclpy.spin(Robot1Publisher())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# robot2_pub

import rclpy
import math

from rclpy.node import Node
from std_msgs.msg import String

class Robot2Publisher(Node):
    def __init__(self):
        super().__init__('robot2_publisher')

        self.pub = self.create_publisher(
            String,
            '/robot2_position',
            10
        )

        self.t = 0.0

        self.create_timer(0.5, self.publish_pos)

        self.get_logger().info('Robot 2 publisher started.')

    def publish_pos(self):
        x = 1.0 * math.cos(self.t + math.pi)
        y = 1.0 * math.sin(self.t + math.pi)

        self.t += 0.2

        msg = String()
        msg.data = f'{x:.2f},{y:.2f}'

        self.pub.publish(msg)

        self.get_logger().info(
            f'Robot2: ({x:.2f}, {y:.2f})'
        )


def main():
    rclpy.init()
    rclpy.spin(Robot2Publisher())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# distance_monitor

import rclpy
import math

from rclpy.node import Node
from std_msgs.msg import String

ALERT_DISTANCE = 2.0

class DistanceMonitor(Node):
    def __init__(self):
        super().__init__('distance_monitor')

        self.pos1 = (0.0, 0.0)
        self.pos2 = (0.0, 0.0)

        self.create_subscription(
            String,
            '/robot1_position',
            self.cb_robot1,
            10
        )

        self.create_subscription(
            String,
            '/robot2_position',
            self.cb_robot2,
            10
        )

        self.get_logger().info('Distance Monitor started.')

    def _parse(self, msg):
        x, y = msg.data.split(',')
        return float(x), float(y)

    def _check_distance(self):
        x1, y1 = self.pos1
        x2, y2 = self.pos2

        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        if dist < ALERT_DISTANCE:
            self.get_logger().warn(
                f'*** PROXIMITY ALERT *** dist={dist:.2f} m < {ALERT_DISTANCE} m'
            )
        else:
            self.get_logger().info(
                f'Distance: {dist:.2f} m [OK]'
            )

    def cb_robot1(self, msg):
        self.pos1 = self._parse(msg)
        self._check_distance()

    def cb_robot2(self, msg):
        self.pos2 = self._parse(msg)
        self._check_distance()


def main():
    rclpy.init()
    rclpy.spin(DistanceMonitor())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
