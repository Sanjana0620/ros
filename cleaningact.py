# ex4_cleaning_server

import rclpy
import time

from rclpy.node import Node
from rclpy.action import (
    ActionServer,
    CancelResponse,
    GoalResponse
)

from custom_interfaces.action import CleaningTask

class CleaningServer(Node):

    def __init__(self):
        super().__init__('cleaning_server')

        ActionServer(
            self,
            CleaningTask,
            'cleaning_task',
            execute_callback=self.execute_goal,
            goal_callback=self.goal_cb,
            cancel_callback=self.cancel_cb
        )

        self.get_logger().info(
            'Cleaning Task Server ready.'
        )

    def goal_cb(self, goal_request):

        self.get_logger().info(
            'Goal received — accepting.'
        )

        return GoalResponse.ACCEPT

    def cancel_cb(self, goal_handle):

        self.get_logger().info(
            'Cancel request received — accepting.'
        )

        return CancelResponse.ACCEPT

    def execute_goal(self, goal_handle):

        steps = goal_handle.request.total_steps

        fb = CleaningTask.Feedback()

        progress = 0

        for step in range(1, steps + 1):

            if goal_handle.is_cancel_requested:

                goal_handle.canceled()

                result = CleaningTask.Result()

                result.final_progress = progress

                result.outcome = (
                    f'CANCELLED at {progress}%'
                )

                self.get_logger().info(
                    result.outcome
                )

                return result

            time.sleep(0.6)

            progress = step * (100 // steps)

            fb.progress_percent = progress

            goal_handle.publish_feedback(fb)

            self.get_logger().info(
                f'Progress: {progress}%'
            )

        goal_handle.succeed()

        result = CleaningTask.Result()

        result.final_progress = 100
        result.outcome = 'COMPLETED'

        return result


def main():
    rclpy.init()

    rclpy.spin(CleaningServer())

    rclpy.shutdown()


if __name__ == '__main__':
    main()



# ex4_cleaning_client

import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient
from custom_interfaces.action import CleaningTask

class CleaningClient(Node):

    def __init__(self):
        super().__init__('cleaning_client')

        self._client = ActionClient(
            self,
            CleaningTask,
            'cleaning_task'
        )

        self._gh = None

        self._client.wait_for_server()

        goal = CleaningTask.Goal()

        goal.total_steps = 10

        self.get_logger().info(
            'Sending cleaning goal (10 steps).'
        )

        future = self._client.send_goal_async(
            goal,
            feedback_callback=self.on_feedback
        )

        future.add_done_callback(
            self.goal_response_cb
        )

    def goal_response_cb(self, future):

        self._gh = future.result()

        if not self._gh.accepted:

            self.get_logger().info(
                'Goal rejected!'
            )

            return

        self.get_logger().info(
            'Goal accepted.'
        )

        result_future = self._gh.get_result_async()

        result_future.add_done_callback(
            self.result_cb
        )

    def on_feedback(self, msg):

        pct = msg.feedback.progress_percent

        self.get_logger().info(
            f'Cleaning progress: {pct}%'
        )

        if pct > 50 and self._gh is not None:

            self.get_logger().info(
                '> 50% — cancelling goal!'
            )

            self._gh.cancel_goal_async()

            self._gh = None

    def result_cb(self, future):

        res = future.result().result

        self.get_logger().info(
            f'Final result: {res.outcome} '
            f'(progress = {res.final_progress}%)'
        )


def main():
    rclpy.init()

    node = CleaningClient()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
