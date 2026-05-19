# ex5_speed_server

import rclpy

from rclpy.node import Node
from custom_interfaces.srv import SetSpeed
from std_msgs.msg import Float64

MAX_SPEED = 5.0
SLOW_CAP = 1.0

VALID_MODES = {'NORMAL', 'SLOW'}

class SpeedServer(Node):

    def __init__(self):
        super().__init__('speed_server')

        self.current_speed = 0.0

        self.create_service(
            SetSpeed,
            'set_speed',
            self.handle_request
        )

        self.pub = self.create_publisher(
            Float64,
            '/current_speed',
            10
        )

        self.create_timer(
            0.5,
            self.publish_speed
        )

        self.get_logger().info(
            'Speed Server ready.'
        )

    def handle_request(self, req, res):

        mode = req.mode.strip().upper()

        if mode not in VALID_MODES:

            res.accepted = False
            res.actual_speed = self.current_speed

            res.message = (
                f'Unknown mode: {mode}. Use NORMAL or SLOW.'
            )

            self.get_logger().warn(res.message)

            return res

        if req.speed < 0.0 or req.speed > MAX_SPEED:

            res.accepted = False
            res.actual_speed = self.current_speed

            res.message = (
                f'Speed {req.speed} out of range [0, {MAX_SPEED}]'
            )

            self.get_logger().warn(res.message)

            return res

        cap = SLOW_CAP if mode == 'SLOW' else MAX_SPEED

        self.current_speed = min(req.speed, cap)

        res.accepted = True
        res.actual_speed = self.current_speed

        res.message = (
            f'Speed set to {self.current_speed:.2f} m/s [{mode}]'
        )

        self.get_logger().info(res.message)

        return res

    def publish_speed(self):

        msg = Float64()

        msg.data = self.current_speed

        self.pub.publish(msg)


def main():
    rclpy.init()
    rclpy.spin(SpeedServer())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# ex5_speed_client

import rclpy
import sys

from rclpy.node import Node
from custom_interfaces.srv import SetSpeed
from std_msgs.msg import Float64

class SpeedClient(Node):

    def __init__(self):
        super().__init__('speed_client')

        if len(sys.argv) != 3:
            print(
                'Usage: ros2 run service_exercises speed_client'
                ' <speed_m/s> <NORMAL|SLOW>'
            )
            return

        cli = self.create_client(
            SetSpeed,
            'set_speed'
        )

        cli.wait_for_service()

        req = SetSpeed.Request()

        req.speed = float(sys.argv[1])
        req.mode = sys.argv[2]

        future = cli.call_async(req)

        rclpy.spin_until_future_complete(self, future)

        res = future.result()

        if not res.accepted:

            self.get_logger().warn(
                f'Rejected: {res.message}'
            )

            return

        self.get_logger().info(
            f'Accepted: {res.message}'
            f' | actual = {res.actual_speed:.2f} m/s'
        )

        self.create_subscription(
            Float64,
            '/current_speed',
            self.speed_cb,
            10
        )

        self.get_logger().info(
            'Listening on /current_speed ...'
        )

    def speed_cb(self, msg):

        self.get_logger().info(
            f'/current_speed = {msg.data:.2f} m/s'
        )


def main():
    rclpy.init()

    node = SpeedClient()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
