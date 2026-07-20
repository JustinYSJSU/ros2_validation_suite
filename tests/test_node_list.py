import pytest
import math
import transforms3d
import time
from config import IMU_RANGES
from rclpy.time import Time
from rclpy.clock import ClockType

class TestNodeList:
    
    def test_node_list(self, node_list_node, config_load):
        '''Test function to validate # of active nodes in ROS 2 system
        Expect the following nodes to be active:
            /battery_publisher_node
            /imu_publisher_node
            /odometry_publisher_node
            /prom_exporter
            /discovery_node
        '''
        time.sleep(3)
        config = config_load('node_config.yaml')['required']
        node_list = [name for name in node_list_node.get_node_names() if not name.startswith('_ros2_daemon')]

        assert set(node_list) == set(expected_nodes)