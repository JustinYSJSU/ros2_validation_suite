import random
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Header
from geometry_msgs.msg import Quaternion # orientation
from geometry_msgs.msg import Vector3 # angular_velocity + linear acceleration
class SensorDataPublisher(Node):
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
        self.imu_quality_dict = self.imu_quality_dict.fromkeys(self.imu_quality_dict, "good")
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
        msg.linear_acceleration = self.generate_linear_accleration(quality=self.imu_quality_dict['linear_acceleration'])
        self.pub.publish(msg)
        return msg

    def generate_imu_header(self):
        msg = Header()
        msg.stamp = self.get_clock().now().to_msg()
        msg.frame_id = "imu_link"
        return msg
    
    def generate_orientation(self, quality):
        print()

    def generate_angular_velocity(self, quality):
        print()

    def generate_linear_accleration(self, quality):
        print()