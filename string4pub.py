# mode_pub

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

MODES = ['AUTO', 'MANUAL']

class ModePub(Node):
    def __init__(self):
        super().__init__('mode_publisher')

        self.pub = self.create_publisher(
            String,
            '/robot_mode',
            10
        )

        self.index = 0

        self.create_timer(3.0, self.publish_mode)

        self.get_logger().info('Mode publisher started.')

    def publish_mode(self):
        msg = String()
        msg.data = MODES[self.index % 2]

        self.pub.publish(msg)

        self.get_logger().info(
            f'Mode: {msg.data}'
        )

        self.index += 1


def main():
    rclpy.init()
    rclpy.spin(ModePub())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# obstacle_pub

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class ObstaclePub(Node):
    def __init__(self):
        super().__init__('obstacle_publisher')

        self.pub = self.create_publisher(
            Int32,
            '/obstacle_count',
            10
        )

        self.count = 0

        self.create_timer(1.0, self.publish_count)

        self.get_logger().info('Obstacle publisher started.')

    def publish_count(self):
        msg = Int32()
        msg.data = self.count

        self.pub.publish(msg)

        self.get_logger().info(
            f'Obstacles: {self.count}'
        )

        self.count = (self.count + 1) % 11


def main():
    rclpy.init()
    rclpy.spin(ObstaclePub())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# fusion_sub

import rclpy

from rclpy.node import Node
from std_msgs.msg import String, Int32

OBSTACLE_THRESHOLD = 5

class FusionSubscriber(Node):
    def __init__(self):
        super().__init__('fusion_subscriber')

        self.mode = 'MANUAL'
        self.obstacles = 0

        self.create_subscription(
            String,
            '/robot_mode',
            self.cb_mode,
            10
        )

        self.create_subscription(
            Int32,
            '/obstacle_count',
            self.cb_obstacles,
            10
        )

        self.get_logger().info('Fusion Subscriber ready.')

    def cb_mode(self, msg):
        self.mode = msg.data
        self._evaluate()

    def cb_obstacles(self, msg):
        self.obstacles = msg.data
        self._evaluate()

    def _evaluate(self):
        if self.mode == 'AUTO' and self.obstacles > OBSTACLE_THRESHOLD:

            self.get_logger().error(
                f'STOP ROBOT | mode={self.mode} | obstacles={self.obstacles}'
            )

        elif self.mode == 'MANUAL':

            self.get_logger().info(
                f'MANUAL MODE | obstacles={self.obstacles} (auto-stop bypassed)'
            )

        else:

            self.get_logger().info(
                f'CONTINUE | mode={self.mode} | obstacles={self.obstacles}'
            )


def main():
    rclpy.init()
    rclpy.spin(FusionSubscriber())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
