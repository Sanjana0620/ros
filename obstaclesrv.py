# ex4_obstacle_server

import rclpy

from rclpy.node import Node
from custom_interfaces.srv import CheckObstacle

class ObstacleServer(Node):

    def __init__(self):
        super().__init__('obstacle_check_server')

        self.threshold = 3.0

        self.create_service(
            CheckObstacle,
            'check_obstacle',
            self.handle_request
        )

        self.get_logger().info(
            f'Obstacle Check Server ready. Threshold = {self.threshold} m'
        )

    def handle_request(self, req, res):

        res.threshold = self.threshold

        if req.distance > self.threshold:

            res.is_clear = True

            res.status = (
                f'CLEAR PATH (dist={req.distance:.2f} m)'
            )

        else:

            res.is_clear = False

            res.status = (
                f'OBSTACLE DETECTED (dist={req.distance:.2f} m)'
            )

        self.get_logger().info(res.status)

        return res


def main():
    rclpy.init()
    rclpy.spin(ObstacleServer())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# ex4_obstacle_client

import rclpy
import sys

from rclpy.node import Node
from custom_interfaces.srv import CheckObstacle

class ObstacleClient(Node):

    def __init__(self):
        super().__init__('obstacle_check_client')

        if len(sys.argv) != 2:
            print(
                'Usage: ros2 run service_exercises obstacle_client'
                ' <distance_metres>'
            )
            return

        cli = self.create_client(
            CheckObstacle,
            'check_obstacle'
        )

        cli.wait_for_service()

        req = CheckObstacle.Request()

        req.distance = float(sys.argv[1])

        future = cli.call_async(req)

        rclpy.spin_until_future_complete(self, future)

        res = future.result()

        log = self.get_logger()

        msg = (
            f'{res.status} [threshold = {res.threshold} m]'
        )

        if res.is_clear:
            log.info(msg)
        else:
            log.warn(msg)


def main():
    rclpy.init()
    ObstacleClient()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
