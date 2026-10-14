import sys
from std_srvs.srv import Trigger
import rclpy
from rclpy.node import Node

class AutoTakeoffClient(Node):

    def __init__(self):
        super().__init__('auto_takeoff_client')
        self.cli = self.create_client(Trigger, 'takeoff')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('takeoff service not available, waiting again...')
        self.req = Trigger.Request()

    def send_request(self):
        return self.cli.call_async(self.req)


def main():
    rclpy.init()

    takeoff_client = AutoTakeoffClient()
    future = takeoff_client.send_request()
    rclpy.spin_until_future_complete(takeoff_client, future)
    response = future.result()
    if response.success:
        takeoff_client.get_logger().info('Server said: %s' % response.message)
    else:
        takeoff_client.get_logger().error('Takeoff refused: %s' % response.message)

    takeoff_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()