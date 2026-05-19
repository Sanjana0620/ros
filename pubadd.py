#pub_num1 
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class PubA(Node):
    def __init__(self):
        super().__init__('publisher_a')

        self.pub = self.create_publisher(Int32, '/num1', 10)
        self.count = 1

        self.create_timer(1.0, self.publish_num)

        self.get_logger().info('Publisher A started on /num1')

    def publish_num(self):
        msg = Int32()
        msg.data = self.count

        self.pub.publish(msg)

        self.get_logger().info(f'/num1 published: {self.count}')

        self.count += 1


def main():
    rclpy.init()
    rclpy.spin(PubA())
    rclpy.shutdown()


if __name__ == '__main__':
    main()


#pubnum2
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class PubB(Node):
    def __init__(self):
        super().__init__('publisher_b')

        self.pub = self.create_publisher(Int32, '/num2', 10)
        self.count = 100

        self.create_timer(1.0, self.publish_num)

        self.get_logger().info('Publisher B started on /num2')

    def publish_num(self):
        msg = Int32()
        msg.data = self.count

        self.pub.publish(msg)

        self.get_logger().info(f'/num2 published: {self.count}')

        self.count += 10


def main():
    rclpy.init()
    rclpy.spin(PubB())
    rclpy.shutdown()


if __name__ == '__main__':
    main()


#addsub
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class AdditionSubscriber(Node):
    def __init__(self):
        super().__init__('addition_subscriber')

        self.num1 = 0
        self.num2 = 0

        self.create_subscription(
            Int32,
            '/num1',
            self.cb_num1,
            10
        )

        self.create_subscription(
            Int32,
            '/num2',
            self.cb_num2,
            10
        )

        self.pub_sum = self.create_publisher(
            Int32,
            '/result_sum',
            10
        )

        self.get_logger().info('Addition Subscriber ready.')

    def cb_num1(self, msg):
        self.num1 = msg.data
        self._publish_sum()

    def cb_num2(self, msg):
        self.num2 = msg.data
        self._publish_sum()

    def _publish_sum(self):
        result = Int32()
        result.data = self.num1 + self.num2

        self.pub_sum.publish(result)

        self.get_logger().info(
            f'{self.num1} + {self.num2} = {result.data}'
        )


def main():
    rclpy.init()
    rclpy.spin(AdditionSubscriber())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
