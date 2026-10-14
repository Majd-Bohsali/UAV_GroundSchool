import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand

class AutoTakeOff(Node):

    def __init__(self):
        super().__init__('autonomous_takeoff')
        self.mode_pub = self.create_publisher(
            OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile_sensor_data)
        self.setpoint_pub = self.create_publisher(
            TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos_profile_sensor_data)
        self.cmd_pub = self.create_publisher(
            VehicleCommand, '/fmu/in/vehicle_command', qos_profile_sensor_data)

        self.target_alt = 10.0

        timer_period = 0.25  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        timeNow = self.get_clock().now().nanoseconds//1000

        self.mode_pub.publish(OffboardControlMode(timestamp=timeNow, position = True))
        self.setpoint_pub.publish(TrajectorySetpoint(timestamp = timeNow, position = [0.0, 0.0, -self.target_alt]))

        if self.i == 10:
            self.send_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0)
            self.send_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0)
            self.get_logger().info('Taking off to %.1f m' % self.target_alt)
        self.i += 1

    def send_command(self, command, p1=0.0, p2=0.0):
        self.cmd_pub.publish(VehicleCommand(
            timestamp=self.get_clock().now().nanoseconds // 1000,
            command=command, param1=p1, param2=p2,
            target_system=1, target_component=1,
            source_system=1, source_component=1, from_external=True))


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = AutoTakeOff()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()