# ex2_command_server

import rclpy

from rclpy.node import Node
from custom_interfaces.srv import RobotCommand

VALID = {'START', 'STOP', 'RESET'}

class CommandServer(Node):

    def __init__(self):
        super().__init__('robot_command_server')

        self.log = []

        self.create_service(
            RobotCommand,
            'robot_command',
            self.handle_request
        )

        self.get_logger().info(
            'Robot Command Server ready.'
        )

    def handle_request(self, req, res):

        cmd = req.command.strip().upper()

        if cmd not in VALID:

            res.success = False

            res.confirmation = (
                f'REJECTED: unknown command "{cmd}"'
            )

            self.get_logger().warn(res.confirmation)

            return res

        if cmd == 'RESET':
            self.log.clear()

        self.log.append(cmd)

        res.success = True

        res.confirmation = (
            f'{cmd} executed successfully.'
        )

        self.get_logger().info(
            f'{cmd} | Log: {self.log}'
        )

        return res


def main():
    rclpy.init()
    rclpy.spin(CommandServer())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# ex2_command_client

import rclpy
import sys

from rclpy.node import Node
from custom_interfaces.srv import RobotCommand

class CommandClient(Node):

    def __init__(self):
        super().__init__('robot_command_client')

        if len(sys.argv) != 2:
            print(
                'Usage: ros2 run service_exercises command_client'
                ' <START|STOP|RESET>'
            )
            return

        cli = self.create_client(
            RobotCommand,
            'robot_command'
        )

        cli.wait_for_service()

        req = RobotCommand.Request()

        req.command = sys.argv[1]

        future = cli.call_async(req)

        rclpy.spin_until_future_complete(self, future)

        res = future.result()

        if res.success:
            self.get_logger().info(
                f'OK : {res.confirmation}'
            )
        else:
            self.get_logger().warn(
                f'FAIL: {res.confirmation}'
            )


def main():
    rclpy.init()
    CommandClient()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
