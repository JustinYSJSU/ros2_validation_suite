#!/usr/bin/env python3
"""prom_exporter.py
ROS 2 node which uses prometheus_client to scrape data from topics, and then expose
the gathered metrics via HTTP
"""

import rclpy
import time
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import Imu, BatteryState
from diagnostic_msgs.msg import DiagnosticStatus
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TwistWithCovariance, PoseWithCovariance, Pose, Point, Quaternion, Vector3, Twist
from prometheus_client import start_http_server, Gauge, Counter
from validation_suite.msg import TelemetryImu, TelemetryOdometry

class PromExporter(Node):
    def __init__(self):
        super().__init__("prom_exporter")
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.create_subscription(msg_type=Imu, topic="imu_data", callback=self.callback, qos_profile=qos)
        self.create_subscription(msg_type=Odometry, topic="odometry_data", callback=self.odometry_callback, qos_profile=qos)
        self.create_subscription(msg_type=BatteryState, topic="battery_data", callback=self.battery_callback, qos_profile=qos)
        self.create_subscription(msg_type=TelemetryImu, topic="telemetry_imu", callback=self.telemetry_imu_callback, qos_profile=qos)
        self.create_subscription(msg_type=TelemetryOdometry, topic="telemetry_odometry", callback=self.telemetry_odometry_callback, qos_profile=qos)

        self.telemetry_imu_status_count = Counter('imu_status_total', 'Counter for each status',
        ['status'])
        self.telemetry_imu_current_status = Gauge('telemetry_imu_current_status','Current msg status')
        self.telemetry_imu_freq = Gauge('telemetry_imu_freq', 'Imu msg freq')

        self.telemetry_imu_angular_velocity_x = Gauge('telemetry_imu_angular_velocity_x', 'msg angular velocity x')
        self.telemetry_imu_angular_velocity_y = Gauge('telemetry_imu_angular_velocity_y', 'msg angular velocity y')
        self.telemetry_imu_angular_velocity_z = Gauge('telemetry_imu_angular_velocity_z', 'msg angular velocity z')

        self.telemetry_imu_linear_acceleration_x = Gauge('telemetry_imu_linear_acceleration_x', 'msg linear accelearation x')
        self.telemetry_imu_linear_acceleration_y = Gauge('telemetry_imu_linear_acceleration_y', 'msg linear accelearation y')
        self.telemetry_imu_linear_acceleration_z = Gauge('telemetry_imu_linear_acceleration_z', 'msg linear accelearation z')

        self.telemetry_imu_orientation_x = Gauge('telemetry_imu_orientation_x', 'msg orientation x')
        self.telemetry_imu_orientation_y = Gauge('telemetry_imu_orientation_y', 'msg orientation y')
        self.telemetry_imu_orientation_z = Gauge('telemetry_imu_orientation_z', 'msg orientation z')

        self.telemetry_odometry_status_count = Counter('odometry_status_total', 'Counter for each status',
        ['status'])
        self.telemetry_odometry_current_status = Gauge('telemetry_odometry_current_status','Current msg status')
        self.telemetry_odometry_freq = Gauge('telemetry_odometry_freq', 'Odometry msg freq')

        self.telemetry_odometry_pose_x = Gauge('telemetry_odometry_pose_x', 'msg pose x')
        self.telemetry_odometry_pose_y = Gauge('telemetry_odometry_pose_y', 'msg pose y')
        self.telemetry_odometry_pose_z = Gauge('telemetry_odometry_pose_z', 'msg pose z')

        self.telemetry_odometry_orientation_x = Gauge('telemetry_odometry_orientation_x', 'msg orientation x')
        self.telemetry_odometry_orientation_y = Gauge('telemetry_odometry_orientation_y', 'msg orientation y')
        self.telemetry_odometry_orientation_z = Gauge('telemetry_odometry_orientation_z', 'msg orientation z')

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

        self.battery_percentage = Gauge('battery_percentage', 'Battery Percentage')
        self.battery_voltage = Gauge('battery_voltage', 'Battery Voltage')

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

        self.pose_x.set(msg.pose.pose.position.x)
        self.pose_y.set(msg.pose.pose.position.y)
        self.pose_z.set(msg.pose.pose.position.z)

        self.odo_orientation_x.set(msg.pose.pose.orientation.x)
        self.odo_orientation_y.set(msg.pose.pose.orientation.y)
        self.odo_orientation_z.set(msg.pose.pose.orientation.z)
        
    def battery_callback(self, msg):
        """Set PromExporter node values to received metrics from topic msg

        Args: msg (sensor_msgs.msg - BatteryState): The given BatteryState message
        """
        self.battery_percentage.set(msg.percentage)
        self.battery_voltage.set(msg.voltage)
        
    def telemetry_imu_callback(self, msg):
        """Set PromExporter node values to received metrics from topic msg

        Args: msg (TelemetryImu): The given TelemetryImu message
        """
        self.telemetry_imu_angular_velocity_x.set(msg.angular_velocity_x)
        self.telemetry_imu_angular_velocity_y.set(msg.angular_velocity_y)
        self.telemetry_imu_angular_velocity_z.set(msg.angular_velocity_z)

        self.telemetry_imu_linear_acceleration_x.set(msg.linear_acceleration_x)
        self.telemetry_imu_linear_acceleration_y.set(msg.linear_acceleration_y)
        self.telemetry_imu_linear_acceleration_z.set(msg.linear_acceleration_z)

        self.telemetry_imu_orientation_x.set(msg.orientation_x)
        self.telemetry_imu_orientation_x.set(msg.orientation_y)
        self.telemetry_imu_orientation_x.set(msg.orientation_z)

        if msg.status == 'GOOD':
            self.telemetry_imu_current_status.set(1)
            self.telemetry_imu_status_count.labels(status="GOOD").inc()
        elif msg.status == 'WARN':
            self.telemetry_imu_current_status.set(2)
            self.telemetry_imu_status_count.labels(status="WARN").inc()
        else:
            self.telemetry_imu_current_status.set(3)
            self.telemetry_imu_status_count.labels(status="POOR").inc()
        self.telemetry_imu_freq.set(msg.message_rate_hz)
    
    def telemetry_odometry_callback(self, msg):
        """Set PromExporter node values to received metrics from topic msg

        Args: msg (TelemetryOdometry): The given TelemetryOdometry message
        """
        self.telemetry_odometry_pose_x.set(msg.odometry_pose_x)
        self.telemetry_odometry_pose_y.set(msg.odometry_pose_y)
        self.telemetry_odometry_pose_z.set(msg.odometry_pose_z)

        self.telemetry_odometry_orientation_x.set(msg.odometry_orientation_x)
        self.telemetry_odometry_orientation_y.set(msg.odometry_orientation_y)
        self.telemetry_odometry_orientation_z.set(msg.odometry_orientation_z)

        if msg.status == 'GOOD':
            self.telemetry_odometry_current_status.set(1)
            self.telemetry_odometry_status_count.labels(status="GOOD").inc()
        elif msg.status == 'WARN':
            self.telemetry_odometry_current_status.set(2)
            self.telemetry_odometry_status_count.labels(status="WARN").inc()
        else:
            self.telemetry_odometry_current_status.set(3)
            self.telemetry_odometry_status_count.labels(status="POOR").inc()
        self.telemetry_odometry_freq.set(msg.message_rate_hz)

def main():
    rclpy.init()
    start_http_server(8000)
    node = PromExporter()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
