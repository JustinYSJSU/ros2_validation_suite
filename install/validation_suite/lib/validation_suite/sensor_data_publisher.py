#!/usr/bin/python3
"""
sensor_data_publisher.py

ROS2 sensor data publisher node for the IMU Sensor Validation Framework.
Generates simulated IMU data with configurable quality levels (good/warn/poor)
and publishes to the 'imu_data' topic at 0.5s intervals.

Part of: ROS2 Sensor Validation & Testing Framework
"""
import random
import rclpy
import transforms3d
import math
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Header
from geometry_msgs.msg import Quaternion # orientation
from geometry_msgs.msg import Vector3 # angular_velocity + linear acceleration

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

class SensorDataPublisher(Node):
    """
    Publishes simulated IMU sensor data with probabilistic fault injection.
    
    Publishes good data 85% of the time, degraded (warn) 10%, 
    and failed (poor) 5%. Fault injection targets a single randomly 
    selected component per message.
    
    Topics:
        /imu_data (sensor_msgs/Imu)
    """
    def __init__(self):
        super().__init__("sensor_data_publisher_node")
        self.pub = self.create_publisher(Imu, "imu_data", 10)
        self.time = self.create_timer(0.5, self.generate_imu_data)
        self.imu_property_dict = {
            1: "orientation",
            2: "angular_velocity",
            3: "linear_acceleration"
        }
        self.imu_quality_dict = {
            "orientation": "good",
            "angular_velocity": "good",
            "linear_acceleration": "good"
        }

    def generate_imu_data(self):
        """
        Calculates the quality level (good/warn/poor), then
        generates the appropriate IMU data

        Args:
            N/A

        Returns:
            msg: Valid, generaged message with appropriate quality-level data
        """
        self.imu_quality_dict = self.imu_quality_dict.fromkeys(self.imu_quality_dict, "good") # reset quality dict before each msg
        msg = Imu()
        msg.header = self.generate_imu_header()
        status_probability = round(random.random(), 2)

        if status_probability < 0.85: # "good" quality data
            pass
        elif 0.85 <= status_probability < 0.95: # "warning" quality data
            impacted_property = self.imu_property_dict[random.randint(1,3)]
            self.imu_quality_dict[impacted_property] = 'warn'
        else: # "poor" quality data
            impacted_property = self.imu_property_dict[random.randint(1,3)]
            self.imu_quality_dict[impacted_property] = 'poor'
        
        msg.orientation = self.generate_orientation(quality=self.imu_quality_dict['orientation'])
        msg.angular_velocity = self.generate_angular_velocity(quality=self.imu_quality_dict['angular_velocity'])
        msg.linear_acceleration = self.generate_linear_acceleration(quality=self.imu_quality_dict['linear_acceleration'])
        self.pub.publish(msg)
        return msg

    def generate_imu_header(self):
        """
        Generates header for IMU message

        Args:
            N/A

        Returns:
            msg: Valid, generated header
        """
        head = Header()
        head.stamp = self.get_clock().now().to_msg()
        head.frame_id = "imu_link"
        return head
    
    def generate_orientation(self, quality):
        """
        Generates a simulated quaternion orientation.

        Args:
            quality (str): Data quality level - 'good', 'warn', or 'poor'
        
        Returns:
            Quaternion: Valid unit quaternion within ranges defined by quality level
        """
        roll_deg = random.uniform(*IMU_RANGES['orientation'][quality]['roll'])
        pitch_deg = random.uniform(*IMU_RANGES['orientation'][quality]['pitch'])
        yaw_deg   = random.uniform(*IMU_RANGES['orientation'][quality]['yaw'])

        roll_rads = math.radians(roll_deg)
        pitch_rads = math.radians(pitch_deg)
        yaw_rads = math.radians(yaw_deg)

        w, x, y, z = transforms3d.euler.euler2quat(roll_rads, pitch_rads, yaw_rads, axes='sxyz')

        quat = Quaternion()
        quat.w = w
        quat.x = x
        quat.y = y
        quat.z = z

        return quat

    def generate_angular_velocity(self, quality):
        """
        Generates a simulated angular velocity vector.

        Args:
            quality (str): Data quality level - 'good', 'warn', or 'poor'
        
        Returns:
            Vector3: Valid vector (rad/s) within ranges defined by quality level
        """
        x_cord = random.uniform(*IMU_RANGES['angular_velocity'][quality]['x'])
        y_cord = random.uniform(*IMU_RANGES['angular_velocity'][quality]['y'])
        z_cord = random.uniform(*IMU_RANGES['angular_velocity'][quality]['z'])

        vector = Vector3()
        vector.x = x_cord
        vector.y = y_cord
        vector.z = z_cord

        return vector

    def generate_linear_acceleration(self, quality):
        """
        Generates a simulated linear acceleration vector.

        Args:
            quality (str): Data quality level - 'good', 'warn', or 'poor'
        
        Returns:
            Vector3: Valid vector (m/s^2) within ranges defined by quality level
        """
        x_accel = random.uniform(*IMU_RANGES['linear_acceleration'][quality]['x'])
        y_accel = random.uniform(*IMU_RANGES['linear_acceleration'][quality]['y'])
        z_accel = random.uniform(*IMU_RANGES['linear_acceleration'][quality]['z'])

        vector = Vector3()
        vector.x = x_accel
        vector.y = y_accel
        vector.z = z_accel

        return vector

    
def main():
    rclpy.init() # initialize ros2 communication
    my_pub = SensorDataPublisher()
    print("Publishing")

    try:
        rclpy.spin(my_pub) # run until interrupt via keyboard
    except KeyboardInterrupt:
        print("Terminating node...")
        my_pub.destroy_node()

if __name__ == '__main__':
        main()