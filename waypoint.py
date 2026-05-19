# ex3_waypoint_server

import rclpy
import time

from rclpy.node import Node
from rclpy.action import ActionServer
from custom_interfaces.action import WaypointNav

class WaypointServer(Node):

    def __init__(self):
        super().__init__('waypoint_server')

        ActionServer(
            self,
            WaypointNav,
            'waypoint_nav',
            self.execute_goal
        )

        self.get_logger().info(
            'Waypoint Navigation Server ready.'
        )

    def execute_goal(self, goal_handle):

        total = goal_handle.request.total_waypoints

        self.get_logger().info(
            f'Goal: navigate {total} waypoints.'
        )

        fb = WaypointNav.Feedback()

        for wp in range(1, total + 1):

            time.sleep(0.8)

            fb.current_waypoint = wp

            goal_handle.publish_feedback(fb)

            self.get_logger().info(
                f'Waypoint {wp} / {total} reached.'
            )

        goal_handle.succeed()

        result = WaypointNav.Result()

        result.waypoints_completed = total

        return result


def main():
    rclpy.init()

    rclpy.spin(WaypointServer())

    rclpy.shutdown()


if __name__ == '__main__':
    main()



# ex3_waypoint_client

import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient
from custom_interfaces.action import WaypointNav

class WaypointClient(Node):

    def __init__(self, num_wp):
        super().__init__('waypoint_client')

        self._client = ActionClient(
            self,
            WaypointNav,
            'waypoint_nav'
        )

        self._client.wait_for_server()

        goal = WaypointNav.Goal()

        goal.total_waypoints = num_wp

        self.get_logger().info(
            f'Sending goal: {num_wp} waypoints.'
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
            f'Navigation complete. '
            f'Waypoints completed: '
            f'{res.waypoints_completed}'
        )

    def on_feedback(self, msg):

        self.get_logger().info(
            f'Reached waypoint '
            f'{msg.feedback.current_waypoint}'
        )


def main():
    rclpy.init()

    WaypointClient(4)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
