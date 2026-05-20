# cleaning_client

#!/usr/bin/env python3

import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient
from custom_interfaces.action import CleaningTask


class CleaningClient(Node):

    def __init__(self):

        super().__init__('cleaning_client')

        self.cancel_sent = False

        self.client = ActionClient(
            self,
            CleaningTask,
            'cleaning_task'
        )

        self.get_logger().info(
            'Client Ready! Waiting for Server!'
        )

        self.client.wait_for_server()

        self.get_logger().info(
            'Server Found!'
        )

        goal = CleaningTask.Goal()

        goal.total_steps = 10

        future = self.client.send_goal_async(
            goal,
            feedback_callback=self.feedback_cb
        )

        rclpy.spin_until_future_complete(
            self,
            future
        )

        self.response = future.result()

        result_future = self.response.get_result_async()

        rclpy.spin_until_future_complete(
            self,
            result_future
        )

        result = result_future.result().result

        self.get_logger().info(
            f'Final Progress: {result.final_progress}%'
        )

        self.get_logger().info(
            f'Outcome: {result.outcome}'
        )

    def feedback_cb(self, fb):

        progress = fb.feedback.progress_percent

        self.get_logger().info(
            f'Progress: {progress}%'
        )

        if progress > 50 and not self.cancel_sent:

            self.cancel_sent = True

            self.get_logger().info(
                'Canceling Task...'
            )

            self.response.cancel_goal_async()


def main(args=None):

    rclpy.init(args=args)

    CleaningClient()

    rclpy.shutdown()


if __name__ == '__main__':
    main()



# cleaning_server

#!/usr/bin/env python3

import rclpy
import time

from rclpy.node import Node
from rclpy.action import (
    ActionServer,
    CancelResponse
)

from rclpy.executors import MultiThreadedExecutor

from custom_interfaces.action import CleaningTask


class CleaningServer(Node):

    def __init__(self):

        super().__init__('cleaning_server')

        self.server = ActionServer(
            self,
            CleaningTask,
            'cleaning_task',
            self.cb,
            cancel_callback=self.cancel_cb
        )

        self.get_logger().info(
            'Cleaning Server Ready'
        )

    def cancel_cb(self, goal):

        self.get_logger().info(
            'Cancel Request Accepted'
        )

        return CancelResponse.ACCEPT

    def cb(self, goal):

        total = goal.request.total_steps

        feedback = CleaningTask.Feedback()

        for step in range(1, total + 1):

            time.sleep(1)

            progress = int((step / total) * 100)

            if goal.is_cancel_requested:

                self.get_logger().info(
                    'Cleaning Task Canceled'
                )

                goal.canceled()

                result = CleaningTask.Result()

                result.final_progress = progress

                result.outcome = 'CANCELED'

                return result

            feedback.progress_percent = progress

            goal.publish_feedback(feedback)

            self.get_logger().info(
                f'Cleaning Progress: {progress}%'
            )

        goal.succeed()

        self.get_logger().info(
            'Cleaning Completed'
        )

        result = CleaningTask.Result()

        result.final_progress = 100

        result.outcome = 'COMPLETED'

        return result


def main(args=None):

    rclpy.init(args=args)

    node = CleaningServer()

    executor = MultiThreadedExecutor()

    executor.add_node(node)

    executor.spin()

    rclpy.shutdown()


if __name__ == '__main__':
    main()


