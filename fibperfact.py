# ex5_fibperf_server

import rclpy
import time

from rclpy.node import Node
from rclpy.action import ActionServer
from custom_interfaces.action import FibonacciPerf

class FibPerfServer(Node):

    def __init__(self):
        super().__init__('fibperf_server')

        self._server = ActionServer(
            self,
            FibonacciPerf,
            'fibonacci_perf',
            self.execute_goal
        )

        self.get_logger().info(
            'Fibonacci Perf Server ready.'
        )

    def execute_goal(self, goal_handle):

        order = goal_handle.request.order

        self.get_logger().info(
            f'Goal: compute {order} Fibonacci numbers.'
        )

        fb = FibonacciPerf.Feedback()

        if order <= 0:
            seq = []

        elif order == 1:
            seq = [0]

        else:
            seq = [0, 1]

        t0 = time.perf_counter()

        for i in range(2, order):

            seq.append(seq[-1] + seq[-2])

            elapsed_ms = int(
                (time.perf_counter() - t0) * 1000
            )

            fb.partial_sequence = list(seq)
            fb.elapsed_ms = elapsed_ms

            goal_handle.publish_feedback(fb)

            self.get_logger().info(
                f'Step {i}: {seq} | {elapsed_ms} ms'
            )

        total_s = time.perf_counter() - t0

        speed = len(seq) / total_s if total_s > 0 else 0.0

        goal_handle.succeed()

        result = FibonacciPerf.Result()

        result.sequence = list(seq)
        result.speed_per_second = speed

        self.get_logger().info(
            f'Done. Speed: {speed:.2f} numbers/sec'
        )

        return result


def main():
    rclpy.init()

    rclpy.spin(FibPerfServer())

    rclpy.shutdown()


if __name__ == '__main__':
    main()



# ex5_fibperf_client

import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient
from custom_interfaces.action import FibonacciPerf

class FibPerfClient(Node):

    def __init__(self, order):
        super().__init__('fibperf_client')

        self._client = ActionClient(
            self,
            FibonacciPerf,
            'fibonacci_perf'
        )

        self._client.wait_for_server()

        goal = FibonacciPerf.Goal()

        goal.order = order

        self.get_logger().info(
            f'Goal: compute {order} Fibonacci numbers with timing.'
        )

        future = self._client.send_goal_async(
            goal,
            feedback_callback=self.on_feedback
        )

        rclpy.spin_until_future_complete(self, future)

        result_future = future.result().get_result_async()

        rclpy.spin_until_future_complete(
            self,
            result_future
        )

        result = result_future.result().result

        self.get_logger().info(
            f'Final sequence: {result.sequence}'
        )

        self.get_logger().info(
            f'Speed: {result.speed_per_second:.2f} numbers/sec'
        )

    def on_feedback(self, msg):

        fb = msg.feedback

        self.get_logger().info(
            f'Feedback → {fb.partial_sequence} | {fb.elapsed_ms} ms'
        )


def main():
    rclpy.init()

    FibPerfClient(10)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
