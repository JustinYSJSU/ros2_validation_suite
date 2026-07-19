"""odometry_publisher.py

Generates simulated IMU data with configurable quality levels (good/warn/poor)
and publishes to the 'odometry_data' topic at 0.5s intervals.
"""

import random
import rclpy
import transforms3d
import math
import config
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Header
from geometry_msgs.msg import TwistWithCovariance
from geometry_msgs.msg import PoseWithCovariance

class OdometryPublisher(Node):
    """Publishes simulated odometry data with probabilistic fault injection.
    Publishes good data 85% of the time, degraded (warn) 10%, 
    and failed (poor) 5%. Fault injection targets a single randomly 
    selected component per message.

        Topics:
            /odometry_data
    """
    super().__init__("odometry_publisher")
    self.twist_pub = self.create_publisher(TwistWithCovariance, "odometry_twist", self.publish_twist, 10)
    self.post_pub = self.create_publisher(PoseWithConvariance, "odometry_pose", self.publish_pose, 10)
    self.time_twist = self.timer(0.5, self.generate_twist_data)
    self.pose_twist = self.time(0.5, self.generate_pose_data)

    self.pose_property_dict = {
            1: "position",
    }
    self.pose_quality_dict = {
        "position": "good",
    }

    self.twist_property_dict = {
        1: "linear_velocity",
        2: "angular_velocity"
    }
    self.twist_property_dict = {
        "linear_velocity": "good",
        "angular_velocity": "good"
    }