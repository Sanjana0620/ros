# ex1_move_server

import rclpy
import time

from rclpy.node import Node
from rclpy.action import ActionServer
from custom_interfaces.action import MoveRobot

class MoveRobotServer(Node):

    def __init__(self):
        super().__init__('move_robot_server')

        ActionServer(
            self,
            MoveRobot,
            'move_robot',
            self.execute_goal
        )

        self.get_logger().info(
            'Move Robot Action Server ready.'
        )

    def execute_goal(self, goal_handle):

        total = goal_handle.request.total_distance

        self.get_logger().info(
            f'Goal: travel {total} m'
        )

        fb = MoveRobot.Feedback()

        for metre in range(1, total + 1):

            time.sleep(0.5)

            fb.metres_covered = metre

            goal_handle.publish_feedback(fb)

            self.get_logger().info(
                f'Feedback: {metre} / {total} m covered'
            )

        goal_handle.succeed()

        result = MoveRobot.Result()

        result.total_covered = total
        result.status = (
            f'Completed: robot travelled {total} m.'
        )

        return result


def main():
    rclpy.init()

    rclpy.spin(MoveRobotServer())

    rclpy.shutdown()


if __name__ == '__main__':
    main()



# ex1_move_client

import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient
from custom_interfaces.action import MoveRobot

class MoveRobotClient(Node):

    def __init__(self, distance):
        super().__init__('move_robot_client')

        self._client = ActionClient(
            self,
            MoveRobot,
            'move_robot'
        )

        self._client.wait_for_server()

        goal = MoveRobot.Goal()

        goal.total_distance = distance

        self.get_logger().info(
            f'Sending goal: travel {distance} m'
        )

        future = self._client.send_goal_async(
            goal,
            feedback_callback=self.on_feedback
        )

        rclpy.spin_until_future_complete(
            self,
            future
        )

        result_future = future.result().get_result_async()

        rclpy.spin_until_future_complete(
            self,
            result_future
        )

        res = result_future.result().result

        self.get_logger().info(
            f'Result: {res.status} '
            f'({res.total_covered} m)'
        )

    def on_feedback(self, msg):

        self.get_logger().info(
            f'Feedback: '
            f'{msg.feedback.metres_covered} m covered'
        )


def main():
    rclpy.init()

    MoveRobotClient(5)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
