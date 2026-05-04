#!/usr/bin/python3
"""
sensor_data_alert.py

ROS2 sensor alert node for the IMU Sensor Validation Framework.
Subscribes to the "/imu_diag" topic from sensor_data_validator.py and raises alerts for WARN or ERROR states

Part of: ROS2 Sensor Validation & Testing Framework
"""
from rclpy.node import Node
from diagnostic_msgs.msg import DiagnosticStatus
from std_msgs.msg import String

class SensorDataAlert(Node):
    """
    Subscribes to the "/imu_diag" topic from sensor_data_validator.py and raises alerts for WARN or ERROR states

    Topics:
        Subscribed: "/imu_diag"
    """

    def __init__(self):
        super().__init__("sensor_data_alert_node")
        self.sub = self.create_subscription(DiagnosticStatus, "imu_diag", self.log_alert, 10)
    
    def log_alert(self, msg):
        """
        Callback function for imu_diag topic subscription

        In the case of a WARN or ERROR state, log an alert for the syste,

        Args:
            msg: The given DiagnosticStatus message from topic /imu_diags
        """

        level = msg.level
 
        ros_now = self.get_clock().now().to_msg()  # gives a builtin_interfaces/Time msg
        seconds = ros_now.sec
        nanoseconds = ros_now.nanosec
        dt = datetime.datetime.fromtimestamp(seconds)

        if level == DiagnosticStatus.ERROR:
            self.get_logger().error(f'{dt.strftime("%Y-%m-%d %H:%M:%S")} => ERROR: ')
        elif level == DiagnosticStatus.WARN:
            self.get_logger().warn(f'{dt.strftime("%Y-%m-%d %H:%M:%S")} => WARN: ')