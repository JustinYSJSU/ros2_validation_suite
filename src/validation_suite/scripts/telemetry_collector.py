#!/usr/bin/python3
"""telemetry_imu_collector.py

Subscribe to topic '/imu_data' and collect metrics to be used in telemetry analysis
Publishes custom message TelemetryImu

"""
import rclpy
import transforms3d
import math
import config
from collections import deque
from rclpy.node import Node
from rclpy.time import Time
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from std_msgs.msg import Header
from validation_suite.msg import TelemetryImu

class TelemetryCollector(Node):

    TIMESTAMPS_MIN_LEN = 2
    def __init__(self):
        super().__init__("telemetry_imu_node")
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.imu_timestamps = deque(maxlen=25)
        self.odometry_timestamps = deque(maxlen=25)
        self.pub = self.create_publisher(msg_type=TelemetryImu, topic="/telemetry_imu", qos_profile=qos)
        self.pub = self.create_publisher(msg_type=TelemetryOdometry, topic="/telemetry_odometry", qos_profile=qos)
        self.sub = self.create_subscription(msg_type=Imu, topic="/imu_data", callback=self.imu_callback, qos_profile=qos)
        self.sub = self.create_subscription(msg_type=Odometry, topic="/odometry_data", callback=self.odometry_callback, qos_profile=qos)
    
    def imu_callback(self, msg):
        """
        Receive Imu message from topic '/imu_data' and then
        extract / calculate fields for TelemetryMsg

        Args: The given Imu message

        Returns:
        """
        orientation = msg.orientation
        linear_acceleration = msg.linear_acceleration
        angular_velocity = msg.angular_velocity

        telemetry_msg = TelemetryImu()

        telemetry_msg.angular_velocity_x = msg.angular_velocity.x
        telemetry_msg.angular_velocity_y = msg.angular_velocity.y
        telemetry_msg.angular_velocity_z = msg.angular_velocity.z

        telemetry_msg.orientation_x = msg.orientation.x
        telemetry_msg.orientation_y = msg.orientation.y
        telemetry_msg.orientation_z = msg.orientation.z

        telemetry_msg.linear_acceleration_x = msg.linear_acceleration.x
        telemetry_msg.linear_acceleration_y = msg.linear_acceleration.y
        telemetry_msg.linear_acceleration_z = msg.linear_acceleration.z

        telemetry_msg.msg_age_ms = (self.get_clock().now() - Time.from_msg(msg.header.stamp)).nanoseconds / 1e6

        telemetry_msg.message_rate_hz = self.calculate_freq(timestamps=self.imu_timestamps)
        orientation_result = self.validate_imu_orientation(orientation=orientation)
        angular_velocity_result = self.validate_imu_angular_velocity(angular_velocity=angular_velocity)
        linear_acceleration_result = self.validate_imu_linear_acceleration(linear_acceleration=linear_acceleration)
        telemetry_msg.status = self.overall_status(orientation_status=orientation_result, angular_velocity_status=angular_velocity_result,
        linear_acceleration_status=linear_acceleration_result)

        self.pub.publish(msg=telemetry_msg)

    def calculate_freq(self, timestamps):
        freq = 0.0
        current = self.get_clock().now()
        timestamps.append(current.nanoseconds)

        if len(self.timestamps) >= self.TIMESTAMPS_MIN_LEN:
            elapsed = (timestamps[-1] - timestamps[0]) / 1e9

            if elapsed > 0:
                freq = (len(timestamps) - 1) / elapsed
            else:
                freq = 0.0
        else:
            freq = 0.0
        return freq

    def validate_imu_orientation(self, orientation):
        """Validates a given IMU oritentation

        Args:
            orientation (geometry_msgs.msg): The given IMU orientation
        
        Returns:
            string representing the worst status (ok/warn/poor) of the IMU orientation properties
        """
        x = orientation.x
        y = orientation.y
        z = orientation.z
        w = orientation.w

        magnitude = math.sqrt(x**2 + y**2 + z**2 + w**2)
        if not math.isclose(magnitude, 1.0, abs_tol=1e-3):
            return "POOR"
        roll_rads, pitch_rads, yaw_rads = transforms3d.euler.quat2euler([w, x, y, z], axes='sxyz')

        roll_deg = math.degrees(roll_rads)
        pitch_deg = math.degrees(pitch_rads)
        yaw_deg = math.degrees(yaw_rads)

        return self.get_worst_status(value_tuple=(roll_deg, pitch_deg,yaw_deg), component="orientation", keys=("roll", "pitch", "yaw"))

    def validate_imu_angular_velocity(self, angular_velocity):
        """Validates a given IMU angular velocity

        Args:
            angular_velocity (geometry_msgs.msg - Vector3): The given angular velocity
        """
        x = angular_velocity.x
        y = angular_velocity.y
        z = angular_velocity.z
        return self.get_worst_status(value_tuple=(x,y,z), component="angular_velocity", keys=("x", "y", "z"))

    def validate_imu_linear_acceleration(self, linear_acceleration):
        """Validates a given IMU linear acceleration

        Args:
            linear_acceleration (geometry_msgs.msg - Vector3: The given linear acceleration
        """
        
        x = linear_acceleration.x
        y = linear_acceleration.y
        z = linear_acceleration.z
        return self.get_worst_status(value_tuple=(x,y,z), component="linear_acceleration", keys=("x", "y", "z"))

    def get_worst_status(self, value_tuple, component, keys):
        """Given 3 values (oritentation x/y/z, angular_velocity x/y/z, linear acclearation x/y/z),
        classify each value and return the most severe status message

        Args:
            value_tuple (tuple): A tuple containing all 3 values for a component (x/y/z)
            component (str): The component that x/y/z are associated with (orientation, angular_velocity, linear acceleration)
            keys (tuple): The tuple layout names of the corresponding component ("roll", "pitch", "yaw") / ("x", "y", "z")
        """
        severity = {"GOOD": 0, "WARN": 1, "POOR": 2}
        worst = "GOOD"

        # example zip() => [("roll": xxx), ("pitch": xxx), ("yaw": xxx)]
        for key, value in zip((keys), value_tuple):
            res = self.classify_value(value, component, key)   
            if severity[res] > severity[worst]:
                worst = res
        return worst

    def classify_value(self, value, component, key):
        """Given a value from a component, determine it's status (good/warn/poor)

        Args:
            value (num): The given value from the component
            component (str): The given component of the IMU
            key (str): The specific field name to look up in IMU_RANGES (e.g. "roll", "x"
        """
        good_min, good_max = config.IMU_RANGES[component]["good"][key]
        warn_min, warn_max = config.IMU_RANGES[component]["warn"][key]

        if good_min <= value <= good_max:
            return "GOOD"
        elif warn_min <= value <= warn_max:
            return "WARN"
        else:
            return "POOR"

    def overall_status(self, orientation_status, angular_velocity_status, linear_acceleration_status):
        """Given status strings from orientation, angular velocity, and linear accelearation, take
        the worst one to determine overall msg status

        Args:
            orientation_status (str): Determined orientation status
            angular_velocity_status (str): Determined angular velocity status
            linear_acceleration_status (str): Determined linear acceleration status
        
        Returns:
        """
        status_to_value = {
            "GOOD": 1,
            "WARN": 2, 
            "POOR": 3
        }
        max_status = max(status_to_value[orientation_status], status_to_value[angular_velocity_status], status_to_value[linear_acceleration_status])

        flipped = {value: key for key, value in status_to_value.items()}

        return flipped[max_status]

def main():
    rclpy.init() # initialize ros2 communication
    my_pub = TelemetryImuCollector()
    print("Publishing")

    try:
        rclpy.spin(my_pub) # run until interrupt via keyboard
    except KeyboardInterrupt:
        print("Terminating node...")
        my_pub.destroy_node()

if __name__ == '__main__':
        main()