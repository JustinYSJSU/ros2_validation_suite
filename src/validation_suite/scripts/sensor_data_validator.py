#!/usr/bin/python3
"""
sensor_data_validation.py

ROS2 sensor data validator node for the IMU Sensor Validation Framework.
Subscribes to the "/imu_data" topic from sensor_data_publisher.py and validates that the data is at
an appropriate value given the quality level

Part of: ROS2 Sensor Validation & Testing Framework
"""
import random
import rclpy
import transforms3d
import math
from rclpy.node import Node
from rclpy.time import Time
from sensor_msgs.msg import Imu
from diagnostic_msgs.msg import DiagnosticStatus

IMU_RANGES = {
    "orientation": {
        "good":  {"roll": (-15, 15),  "pitch": (-20, 20),  "yaw": (-180, 180)},
        "warn":  {"roll": (-30, 30),  "pitch": (-35, 35),  "yaw": (-180, 180)},
        "poor":  {"roll": (-90, 90),  "pitch": (-90, 90),  "yaw": (-180, 180)}
    },
    "angular_velocity": {
        "good":  {"x": (-2, 2),   "y": (-2, 2),   "z": (-2, 2)},
        "warn":  {"x": (-5, 5),   "y": (-5, 5),   "z": (-5, 5)},
        "poor":  {"x": (-15, 15), "y": (-15, 15), "z": (-15, 15)}
    },
    "linear_acceleration": {
        "good":  {"x": (-15, 15), "y": (-15, 15), "z": (5, 15)},
        "warn":  {"x": (-20, 20), "y": (-20, 20), "z": (2, 20)},
        "poor":  {"x": (-50, 50), "y": (-50, 50), "z": (-50, 50)}
    }
}

class SensorDataValidator(Node):
    """
    Validates simulated IMU sensor data with probabilistic fault injection.
    
    Subscribes to "/imu_data" topic, and validates that each topic msg
    has appropriate data values given the data quality type (OK/WARN/POOR)

    Publishes a DiagnosticStatus msg containing a "final verdict" of the state
    of the node based on its validation
    
    Topics:
        Subscribed: "/imu_data"
        Published: "/imu_diag"
    """
    def __init__(self):
        super().__init__("sensor_data_validator_node")
        self.sub = self.create_subscription(Imu, "imu_data", self.validate_imu_msg, 10)
        self.pub = self.create_publisher(DiagnosticStatus, "imu_diag", 10)
        
    def validate_imu_msg(self, msg):
        """
        Validates a given IMU message

        Args:
            msg: The given IMU message
        """

        diag_msg = DiagnosticStatus()

        header = msg.header
        orientation = msg.orientation
        angular_velocity = msg.angular_velocity
        linear_acceleration = msg.linear_acceleration

        header_result = self.validate_imu_header(header=header)
        orientation_result = self.validate_imu_orientation(orientation=orientation)
        angular_velocity_result = self.validate_imu_angular_velocity(angular_velocity=angular_velocity)
        linear_acceleration_result = self.validate_imu_linear_acceleration(linear_acceleration=linear_acceleration)

        # True, GOOD, GOOD, GOOD
        diag_msg = DiagnosticStatus()

        diag_msg

    def validate_imu_header(self, header):
        """
        Validates a given IMU header

        Args:
            msg: The given IMU header
        """
        stamp = Time.from_msg(header.stamp)
        frame_id = header.frame_id

        return stamp != Time() and frame_id == "imu_link"

    def validate_imu_orientation(self, orientation):
        """
        Validates a given IMU oritentation

        Args:
            orientation: The given IMU orientation
        """
        x = orientation.x
        y = orientation.y
        z = orientation.z
        w = orientation.w

        magnitude = math.sqrt(x**2 + y**2 + z**2 + w**2)
        if not math.isclose(magnitude, 1.0, abs_tol=1e-6):
            return "POOR"
        roll_rads, pitch_rads, yaw_rads = transforms3d.euler.quat2euler([w, x, y, z], axes='sxyz')

        roll_deg = math.degrees(roll_rads)
        pitch_deg = math.degrees(pitch_rads)
        yaw_deg = math.degrees(yaw_rads)

        return self.get_worst_status(value_tuple=(roll_deg, pitch_deg,yaw_deg), component="orientation", keys=("roll", "pitch", "yaw"))

    def validate_imu_angular_velocity(self, angular_velocity):
        """
        Validates a given IMU angular velocity

        Args:
            angular_velocity: The given angular velocity
        """
        x = angular_velocity.x
        y = angular_velocity.y
        z = angular_velocity.z
        return self.get_worst_status(value_tuple=(x,y,z), component="angular_velocity", keys=("x", "y", "z"))

    def validate_imu_linear_acceleration(self, linear_acceleration):
        """
        Validates a given IMU linear acceleration

        Args:
            linear_acceleration: The given linear acceleration
        """
        
        x = linear_acceleration.x
        y = linear_acceleration.y
        z = linear_acceleration.z
        return self.get_worst_status(value_tuple=(x,y,z), component="linear_acceleration", keys=("x", "y", "z"))

    def get_worst_status(self, value_tuple, component, keys):
        """
        Given 3 values (oritentation x/y/z, angular_velocity x/y/z, linear acclearation x/y/z),
        classify each value and return the most severe status message

        Args:
            value_tuple: A tuple containing all 3 values for a component (x/y/z)
            component: The component that x/y/z are associated with (orientation, angular_velocity, linear acceleration)
            keys: The tuple layout names of the corresponding component ("roll", "pitch", "yaw") / ("x", "y", "z")
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
        """
        Given a value from a component, determine it's status (good/warn/poor)

        Args:
            value: The given value from the component
            component: The given component of the IMU
            key: The specific field name to look up in IMU_RANGES (e.g. "roll", "x"
        """
        good_min, good_max = IMU_RANGES[component]["good"][key]
        warn_min, warn_max = IMU_RANGES[component]["warn"][key]

        if good_min <= value <= good_max:
            return "GOOD"
        elif warn_min <= value <= warn_max:
            return "WARN"
        else:
            return "POOR"
def main():
    rclpy.init()
    my_sub = SensorDataValidator()
    print("Validating")

    try:
        rclpy.spin(my_sub) 
    except KeyboardInterrupt:
        print("Terminating node...")
        my_sub.destroy_node()

if __name__ == '__main__':
        main()