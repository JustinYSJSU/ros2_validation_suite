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
from geometry_msgs.msg import TwistWithCovariance, PoseWithCovariance, Pose, Point, Quaternion

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

        msg.pose = self.generate_odometry_pose(quality=self.pose_quality_dict["position"]) # PoseWithCovarience

        msg.twist = self.generate_odometry_twist()
        self.pub.publish(msg)

    def generate_odometry_header(self):
        """Generates header for odometry message

        Args:
            N/A

        Returns:
            msg (std_msgs.msg - Header): Valid, generated header
        """
        head = Header()
        head.stamp = self.get_clock().now().to_msg()
        head.frame_id = "odometry_link"
        return head

    def generate_odometry_pose(self, quality):
        """Generates a simulated PoseWithCovarience msg

        Args:
            quality (str): Data quality level - 'good', 'warn', or 'poor'
        
        Returns:
            pose (geometry_msgs.msg Pose)
        """
        pose_with_covarience = PoseWithCovariance()

        pose = Pose()
        pose_point = Point()
        pose_quant = Quaternion()

        pose_point.x = random.uniform(*config.POSE_WITH_COVARIANCE_RANGES["point"][quality]["x"])
        pose_point.y = random.uniform(*config.POSE_WITH_COVARIANCE_RANGES["point"][quality]["y"])
        pose_point.z = random.uniform(*config.POSE_WITH_COVARIANCE_RANGES["point"][quality]["z"])

        qx = random.uniform(*ranges["orientation"][quality]["x"])
        qy = random.uniform(*ranges["orientation"][quality]["y"])
        qz = random.uniform(*ranges["orientation"][quality]["z"])
        qw = random.uniform(*ranges["orientation"][quality]["w"])

        # CLAUDE: normalization of quant
        norm = math.sqrt(qx**2 + qy**2 + qz**2 + qw**2)
        if norm == 0.0:
            # Degenerate case (all-zero draw): fall back to identity orientation
            qx, qy, qz, qw = 0.0, 0.0, 0.0, 1.0
            norm = 1.0

        pose_quant.x = qx / norm
        pose_quant.y = qy / norm
        pose_quant.z = qz / norm
        pose_quant.w = qw / norm

        pose.position = pose_point
        pose.orientation = pose_quant

        pose_with_covarience.pose = pose
        pose_with_covarience.covariance[0] = -1.0

        return pose_with_covarience