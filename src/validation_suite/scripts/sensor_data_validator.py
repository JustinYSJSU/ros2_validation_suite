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
        diag_msg = DiagnosticStatus()

        header = msg.header
        oritentation = msg.orientation
        angular_velocity = msg.angular_velocity
        linear_acceleration = msg.linear_acceleration

    def validate_imu_header(self, header):
        stamp = Time.from_msg(header.stamp)
        frame_id = header.frame_id

        return stamp != Time() and frame_id == "imu_link"

    def validate_imu_orientation(self, orientation):
        x = orientation.x
        y = orientation.y
        z = orientation.z
        w = orientation.w

        magnitude = math.sqrt(x**2 + y**2 + z**2 + w**2)
        if not math.isclose(magnitude, 1.0, abs_tol=1e-6):
            return False
        roll_rads, pitch_rads, yaw_rads = transforms3d.euler.quat2euler([w, x, y, z], axes='sxyz')

        roll_deg = math.degrees(roll_rads)
        pitch_deg = math.degrees(pitch_rads)
        yaw_deg = math.degrees(yaw_rads)
        
    def generate_imu_diag(self):
        print('test')

def main():
    rclpy.init() # initialize ros2 communication
    my_sub = SensorDataValidator()
    print("Validating")

    try:
        rclpy.spin(my_sub) # run until interrupt via keyboard
    except KeyboardInterrupt:
        print("Terminating node...")
        my_sub.destroy_node()

if __name__ == '__main__':
        main()