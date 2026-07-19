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