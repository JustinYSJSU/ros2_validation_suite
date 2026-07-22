import pytest
import math
import transforms3d
import time
import rclpy

from rclpy.time import Time
from rclpy.clock import ClockType
from sensor_msgs.msg import Imu, BatteryState
from nav_msgs.msg import Odometry

class TestReceive:

    def test_receive_imu_message(self, node_list_node):
        '''
        Test function to validate IMU messages are able to be received
        '''
        received = False

        def imu_callback(msg):
            nonlocal received
            received = True

        node_list_node.create_subscription(Imu, "/imu_data", imu_callback, 10)
        assert self.wait_for_message(
            node_list_node,
            lambda: received,
            timeout=10
        )

    def test_receive_battery_message(self, node_list_node):
        '''
        Test function to validate BatteryState messages are able to be received
        '''
        received = False

        def battery_callback(msg):
            nonlocal received
            received = True

        node_list_node.create_subscription(BatteryState, "/battery_data", battery_callback, 10)

        assert self.wait_for_message(
            node_list_node,
            lambda: received,
            timeout=10
        )

    def test_receive_odometry_message(self, node_list_node):
        '''
        Test function to validate Odometry messages are able to be received
        '''
        received = False

        def odometry_callback(msg):
            nonlocal received
            received = True

        node_list_node.create_subscription(Odometry, "/odometry_data", odometry_callback, 10)

        assert self.wait_for_message(
            node_list_node,
            lambda: received,
            timeout=10
        )
       
    def wait_for_message(self, node, condition, timeout):
        start = time.time()

        while time.time() - start < timeout:
            rclpy.spin_once(node, timeout_sec=0.1)

        if condition():
            return True

        return False