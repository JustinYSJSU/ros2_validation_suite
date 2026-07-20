import pytest
import math
import transforms3d
import time
from config import IMU_RANGES
from rclpy.time import Time
from rclpy.clock import ClockType

class TestNodeTopicList:
    
    def test_node_list(self, node_list_node, config_load):
        '''Test function to validate the active nodes in ROS 2 system
        Expect the following nodes to be active:
            /battery_publisher_node
            /imu_publisher_node
            /odometry_publisher_node
            /prom_exporter
            /discovery_node
        '''
        time.sleep(3)
        config = config_load('node_config.yaml')['required']
        node_list = [name for name in node_list_node.get_node_names() if not name.startswith('_ros2cli_daemon')]

        assert set(node_list) == set(config)

    def test_topic_list(self, node_list_node, config_load):
        '''Test function to validate the active topics in ROS 2 system
        Expect the following topics to be active:
            /battery_data
            /imu_data
            /odometry_data
            /parameter_events
            /rosout
        '''
        time.sleep(3)
        config = config_load('topic_config.yaml')['required']
        topic_names = [topic[0] for topic in node_list_node.get_topic_names_and_types()]

        assert set(topic_names) == set(config)