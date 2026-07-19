#!/usr/bin/env python3
"""prom_exporter.py
ROS 2 node which uses prometheus_client to scrape data from topics, and then expose
the gathered metrics via HTTP
"""

import rclpy
import time
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import Imu
from diagnostic_msgs.msg import DiagnosticStatus
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TwistWithCovariance, PoseWithCovariance, Pose, Point, Quaternion, Vector3, Twist
from prometheus_client import start_http_server, Gauge, Counter

class PromExporter(Node):
    def __init__(self):
        super().__init__("prom_exporter")
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.create_subscription(Imu, "imu_data", self.callback, qos)
        self.create_subscription(Odometry, "odometry_data", self.odometry_callback, qos)
        self.create_subscription(DiagnosticStatus, "imu_diag", self.status_callback, qos)

        self.statues = Counter('sensor_status_total', 'Counter for each status',
        ['status'])
        self.orientation_x = Gauge('imu_orientation_x', 'IMU orientation x')
        self.orientation_y = Gauge('imu_orientation_y', 'IMU orientation y')
        self.orientation_z = Gauge('imu_orientation_z', 'IMU orientation z')

        self.angular_vel_x = Gauge('imu_angular_velocity_x', 'IMU angular velocity x')
        self.angular_vel_y = Gauge('imu_angular_velocity_y', 'IMU angular velocity y')
        self.angular_vel_z = Gauge('imu_angular_velocity_z', 'IMU angular velocity z')

        self.linear_acc_x = Gauge('imu_linear_acceleration_x', 'IMU linear acceleration x')
        self.linear_acc_y = Gauge('imu_linear_acceleration_y', 'IMU linear acceleration y')
        self.linear_acc_z = Gauge('imu_linear_acceleration_z', 'IMU linear acceleration z')

        self.timestamp = Gauge('timestamp', 'Timstamp')

        self.pose_x = Gauge('odometry_pose_x', 'Odometry Pose X')
        self.pose_y = Gauge('odometry_pose_y', 'Odometry Pose Y')
        self.pose_z = Gauge('odometry_pose_z', 'Odometry Pose Z')

        self.odo_orientation_x = Gauge('odometry_orientation_x', 'Odometry Orientation X')
        self.odo_orientation_y = Gauge('odometry_orientation_y', 'Odometry Orientation Y')
        self.odo_orientation_z = Gauge('odometry_orientation_z', 'Odometry Orientation Z')

    def callback(self, msg):
        """Set PromExporter node values to received metrics from topic msg

        Args: msg (sensor_msgs.msg - Imu): The given IMU message
        """
        self.orientation_x.set(msg.orientation.x)
        self.orientation_y.set(msg.orientation.y)
        self.orientation_z.set(msg.orientation.z)

        self.angular_vel_x.set(msg.angular_velocity.x)
        self.angular_vel_y.set(msg.angular_velocity.y)
        self.angular_vel_z.set(msg.angular_velocity.z)

        self.linear_acc_x.set(msg.linear_acceleration.x)
        self.linear_acc_y.set(msg.linear_acceleration.y)
        self.linear_acc_z.set(msg.linear_acceleration.z)

        self.timestamp.set(time.time())

    def odometry_callback(self, msg):
        """Set PromExporter node values to received metrics from topic msg

        Args: msg (nav_msgs.msg - Odometry): The given Odometry message
        """
        pose = msg.pose

        self.pose_x = msg.pose.point.x
        self.pose_y = msg.pose.point.y
        self.pose_z = msg.pose.point.z

        self.odo_orientation_x = msg.orientation.x
        self.odo_orientation_y = msg.orientation.y
        self.odo_orientation_z = msg.orientation.z
        
    def status_callback(self, msg):
        """Set PromExporter node values to received status value from topic msg

        Args: msg (diagnostic_msgs.msg - DiagnosticStatus): The given status message
        """
        level = msg.level

        if level == DiagnosticStatus.OK:
            self.statues.labels(status='GOOD').inc()
        elif level == DiagnosticStatus.WARN:
            self.statues.labels(status='WARN').inc()
        elif level == DiagnosticStatus.ERROR:
            self.statues.labels(status='ERROR').inc()

def main():
    rclpy.init()
    start_http_server(8000)
    node = PromExporter()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
