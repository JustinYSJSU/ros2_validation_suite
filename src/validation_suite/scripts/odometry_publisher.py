#!/usr/bin/python3

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
from geometry_msgs.msg import TwistWithCovariance, PoseWithCovariance, Pose, Point, Quaternion, Vector3, Twist

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

    def __init__(self):
        super().__init__("odometry_publisher")
        self.pub = self.create_publisher(Odometry, "odometry_data", 10)
        self.time = self.create_timer(0.5, self.generate_odometry_data)

        self.pose_property_dict = {
                1: "position",
                2: "covarience"
        }
        self.pose_quality_dict = {
            "position": "good",
            "covarience": "good"
        }

        self.twist_property_dict = {
            1: "twist",
            2: "covarience"
        }
        self.twist_quality_dict = {
            "twist": "good",
            "covarience": "good"
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
                impacted_subproperty = self.pose_property_dict[random.randint(1, 2)]
                self.pose_quality_dict[impacted_subproperty] = 'warn'
            elif impacted_property == TWIST:
                impacted_subproperty = self.twist_property_dict[random.randint(1, 2)]
                self.twist_quality_dict[impacted_subproperty] = 'warn'
        else:
            impacted_property = random.randint(1, 2)
            if impacted_property == POSE:
                impacted_subproperty = self.pose_property_dict[random.randint(1, 2)]
                self.pose_quality_dict[impacted_subproperty] = 'poor'
            elif impacted_property == TWIST:
                impacted_subproperty = self.twist_property_dict[random.randint(1, 2)]
                self.twist_quality_dict[impacted_subproperty] = 'poor'

        msg.pose = self.generate_odometry_pose(quality=self.pose_quality_dict["position"]) # PoseWithCovarience
        msg.twist = self.generate_odometry_twist(quality=self.twist_quality_dict["twist"]) #TwistWithCovarience
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

        qx = random.uniform(*config.POSE_WITH_COVARIANCE_RANGES["orientation"][quality]["x"])
        qy = random.uniform(*config.POSE_WITH_COVARIANCE_RANGES["orientation"][quality]["y"])
        qz = random.uniform(*config.POSE_WITH_COVARIANCE_RANGES["orientation"][quality]["z"])
        qw = random.uniform(*config.POSE_WITH_COVARIANCE_RANGES["orientation"][quality]["w"])

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

    def generate_odometry_twist(self, quality):
        """Generates a simulated TwistWithCovarience msg

        Args:
            quality (str): Data quality level - 'good', 'warn', or 'poor'
        
        Returns:
            pose (geometry_msgs.msg Pose)
        """
        twist_with_covarience = TwistWithCovariance()
        twist = Twist()
        twist_linear = Vector3()
        twist_angular = Vector3()

        twist_linear.x = random.uniform(*config.TWIST_WITH_COVARIANCE_RANGES["linear_velocity"][quality]["x"])
        twist_linear.y = random.uniform(*config.TWIST_WITH_COVARIANCE_RANGES["linear_velocity"][quality]["y"])
        twist_linear.z = random.uniform(*config.TWIST_WITH_COVARIANCE_RANGES["linear_velocity"][quality]["z"])

        twist_angular.x = random.uniform(*config.TWIST_WITH_COVARIANCE_RANGES["angular_velocity"][quality]["x"])
        twist_angular.y = random.uniform(*config.TWIST_WITH_COVARIANCE_RANGES["angular_velocity"][quality]["y"])
        twist_angular.z = random.uniform(*config.TWIST_WITH_COVARIANCE_RANGES["angular_velocity"][quality]["z"])

        twist.linear = twist_linear
        twist.angular = twist_angular

        twist_with_covarience.twist = twist
        twist_with_covarience.covariance[0] = -1.0

        return twist_with_covarience

def main():
    rclpy.init() # initialize ros2 communication
    my_pub = OdometryPublisher()
    print("Publishing")

    try:
        rclpy.spin(my_pub) # run until interrupt via keyboard
    except KeyboardInterrupt:
        print("Terminating node...")
        my_pub.destroy_node()

if __name__ == '__main__':
        main()