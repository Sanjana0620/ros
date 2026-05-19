# ex3_calc_server

import rclpy

from rclpy.node import Node
from custom_interfaces.srv import SmartCalculator

OPS = {
    'ADD': lambda a, b: a + b,
    'SUB': lambda a, b: a - b,
    'MUL': lambda a, b: a * b,
}

class CalcServer(Node):

    def __init__(self):
        super().__init__('smart_calculator_server')

        self.create_service(
            SmartCalculator,
            'smart_calculator',
            self.handle_request
        )

        self.get_logger().info(
            'Smart Calculator Server ready.'
        )

    def handle_request(self, req, res):

        op = req.operation.strip().upper()

        if op not in OPS:

            res.valid = False
            res.expression = f'Unknown operation: {op}'
            res.result = 0

            self.get_logger().warn(f'Bad op: {op}')

            return res

        res.result = OPS[op](req.a, req.b)

        res.expression = (
            f'{req.a} {op} {req.b} = {res.result}'
        )

        res.valid = True

        self.get_logger().info(res.expression)

        return res


def main():
    rclpy.init()
    rclpy.spin(CalcServer())
    rclpy.shutdown()


if __name__ == '__main__':
    main()



# ex3_calc_client

import rclpy
import sys

from rclpy.node import Node
from custom_interfaces.srv import SmartCalculator

class CalcClient(Node):

    def __init__(self):
        super().__init__('smart_calculator_client')

        if len(sys.argv) != 4:
            print(
                'Usage: ros2 run service_exercises calc_client'
                ' <a> <b> <ADD|SUB|MUL>'
            )
            return

        cli = self.create_client(
            SmartCalculator,
            'smart_calculator'
        )

        cli.wait_for_service()

        req = SmartCalculator.Request()

        req.a = int(sys.argv[1])
        req.b = int(sys.argv[2])
        req.operation = sys.argv[3]

        future = cli.call_async(req)

        rclpy.spin_until_future_complete(self, future)

        res = future.result()

        if res.valid:
            self.get_logger().info(
                f'Result : {res.expression}'
            )
        else:
            self.get_logger().warn(
                f'Error : {res.expression}'
            )


def main():
    rclpy.init()
    CalcClient()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
