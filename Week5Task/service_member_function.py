from std_srvs.srv import Trigger

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand


class AutoTakeOffService(Node):

    def __init__(self):
        super().__init__('auto_takeoff_service')
        self.srv = self.create_service(Trigger, 'takeoff', self.AutoTakeoff_callback)

        self.mode_pub = self.create_publisher(
            OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile_sensor_data)
        self.setpoint_pub = self.create_publisher(
            TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos_profile_sensor_data)
        self.cmd_pub = self.create_publisher(
            VehicleCommand, '/fmu/in/vehicle_command', qos_profile_sensor_data)

        self.target_alt = 10.0
        self.taking_off = False

        timer_period = 0.25  
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0


    def AutoTakeoff_callback(self, request, response):
        if self.taking_off:
            response.success = False
            response.message = 'Already taking off'
        else:
            self.taking_off = True
            self.i = 0
            response.success = True
            response.message = 'Takeoff to %.1f m started' % self.target_alt
        self.get_logger().info(response.message)
        return response

    def timer_callback(self):
        if not self.taking_off:
            return  

        time_now = self.get_clock().now().nanoseconds // 1000
        self.mode_pub.publish(OffboardControlMode(timestamp=time_now, position=True))
        self.setpoint_pub.publish(TrajectorySetpoint(
            timestamp=time_now, position=[0.0, 0.0, -self.target_alt]))

        if self.i == 10:
            self.send_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0)
            self.send_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0)
        self.i += 1

    def send_command(self, command, p1=0.0, p2=0.0):
        self.cmd_pub.publish(VehicleCommand(
            timestamp=self.get_clock().now().nanoseconds // 1000,
            command=command, param1=p1, param2=p2,
            target_system=1, target_component=1,
            source_system=1, source_component=1, from_external=True))

def main():
    rclpy.init()

    minimal_service = AutoTakeOffService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()