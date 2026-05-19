# ex1_distance_server

import rclpy
import math

from rclpy.node import Node
from custom_interfaces.srv import ComputeDistance

class DistanceServer(Node):

    def __init__(self):
        super().__init__('distance_server')

        self.create_service(
            ComputeDistance,
            'compute_distance',
            self.handle_request
        )

        self.get_logger().info(
            'Distance Server ready on /compute_distance'
        )

    def handle_request(self, req, res):

        res.distance = math.sqrt(
            (req.x2 - req.x1)**2 +
            (req.y2 - req.y1)**2
        )

        self.get_logger().info(
            f'({req.x1},{req.y1}) -> ({req.x2},{req.y2})'
            f' = {res.distance:.4f}'
        )

        return res


def main():
    rclpy.init()
    rclpy.spin(DistanceServer())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# ex1_distance_client

import rclpy
import sys

from rclpy.node import Node
from custom_interfaces.srv import ComputeDistance

class DistanceClient(Node):

    def __init__(self):
        super().__init__('distance_client')

        if len(sys.argv) != 5:
            print(
                'Usage: ros2 run service_exercises distance_client'
                ' <x1> <y1> <x2> <y2>'
            )
            return

        x1, y1, x2, y2 = [float(v) for v in sys.argv[1:5]]

        cli = self.create_client(
            ComputeDistance,
            'compute_distance'
        )

        cli.wait_for_service()

        req = ComputeDistance.Request()

        req.x1, req.y1 = x1, y1
        req.x2, req.y2 = x2, y2

        future = cli.call_async(req)

        rclpy.spin_until_future_complete(self, future)

        self.get_logger().info(
            f'Distance = {future.result().distance:.4f} units'
        )


def main():
    rclpy.init()
    DistanceClient()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
