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

POSE = 1
TWIST = 2

class OdometryPublisher(Node):
    """Publishes simulated odometry data with probabilistic fault injection.
    Publishes good data 85% of the time, degraded (warn) 10%, 
    and failed (poor) 5%. Fault injection targets a single randomly 
    selected component per message.

        Topics:
            /odometry_data
    """
    super().__init__("odometry_publisher")
    self.pub = self.create_publisher(Odometry, "odometry_data", self.publish_odometry, 10)
    self.time = self.timer(0.5, self.generate_odometry_data)

    self.pose_property_dict = {
            1: "position",
            2: "covarience"
    }
    self.pose_quality_dict = {
        "position": "good",
        "covarience": "good"
    }

    self.twist_property_dict = {
        1: "linear_velocity",
        2: "angular_velocity",
        3: "linear_convarience",
        4: "angular_covarience"
    }
    self.twist_quality_dict = {
        "linear_velocity": "good",
        "angular_velocity": "good",
        "linear_convarience": "good",
        "angular_covarience": "good"
    }

    def generate_odometry_data(self):
        """Calculates the quality level (good/warn/poor), then
        generates the appropriate Odometry data
        """

        self.pose_quality_dict = self.pose_quality_dict.fromkeys(self.pose_quality_dict, "good")
        self.twist_quality_dict = self.twist_quality_dict.fromkeys(self.twist_quality_dict, "good")

        msg = Odometry()
        msg.header = self.generate_odometry_header()
        msg.child_frame_id = 'odometry'

        status_probability = round(random.random(), 2)

        if status_probability < 0.85:
            pass
        elif 0.85 <= status_probability < 0.95:
            impacted_property = random.randint(1, 2)

            if impacted_property == POSE:
                impacted_subproperty = self.pose_property_dict[randint(1, 2)]
                self.pose_quality_dict[impacted_subproperty] = 'warn'
            elif impacted_property == TWIST:
                impacted_subproperty = self.twist_property_dict[randint(1, 4)]
                self.twist_quality_dict[impacted_subproperty] = 'warn'
        else:
            impacted_property = random.randint(1, 2)
            if impacted_property == POSE:
                impacted_subproperty = self.pose_property_dict[randint(1, 2)]
                self.pose_quality_dict[impacted_subproperty] = 'warn'
            elif impacted_property == TWIST:
                impacted_subproperty = self.twist_property_dict[randint(1, 4)]
                self.twist_quality_dict[impacted_subproperty] = 'warn'

        msg.pose = self.generate_odometry_pose()
        msg.twist = self.generate_odometry_twist()
        self.pub.publish(msg)