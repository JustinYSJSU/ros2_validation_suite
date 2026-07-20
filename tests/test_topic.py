import pytest
import math
import transforms3d
import time
from rclpy.time import Time
from rclpy.clock import ClockType

class TestTopic:

    def test_topic_list(self, node_list_node, config_load):
        '''Test function to validate the active topics in ROS 2 system
        Expect the following topics to be active with the following types
            /battery_data: sensor_msgs/msg/BatteryState
            /imu_data: sensor_msgs/msg/Imu
            /odometry_data: nav_msgs/msg/Odometry
            /parameter_events: rcl_interfaces/msg/ParameterEvent
            /rosout: rcl_interfaces/msg/Log
        '''
        time.sleep(3)
        config = config_load('topic_config.yaml')['required']
        topics = dict(node_list_node.get_topic_names_and_types())

        for topic, expected_type in config.items():
            assert topic in topics.keys(), f"{topic} not found"

            actual_type = topics[topic]

            assert expected_type in actual_type, (
                f"{topic} has wrong type. "
                f"Expected: {expected_type}, "
                f"Actual: {actual_types}"
            )
    
    def test_topic_count(self, node_list_node, config_load):
        '''Test function to validate number of publisher / subscribers per topic
         Expect the following topics to be active with the follwing counts
            /battery_data:
                publisher_count: 1
                subscriber_count: 1
            /imu_data:
                publisher_count: 1
                subscriber_count: 1
            /odometry_data:
                publisher_count: 1
    s           ubscriber_count: 1
        '''
        time.sleep(3)
        config_topics = config_load('topic_config_short.yaml')['required']
        config_counts = config_load('topic_count_config.yaml')['required']

        for topic in config_topics:
            assert node_list_node.count_publishers(topic) == config_counts[topic]['publisher_count']
            assert node_list_node.count_subscribers(topic) == config_counts[topic]['subscriber_count']

