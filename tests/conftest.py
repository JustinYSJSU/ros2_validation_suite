import sys
import os
import pytest
from config import IMU_RANGES
from rclpy.node import Node
from sensor_data_publisher import SensorDataPublisher
from sensor_data_validator import SensorDataValidator
from sensor_data_alert import SensorDataAlert

sys.path.append(os.path.join(os.path.dirname(__file__), '../src/validation_suite/scripts'))

@pytest.fixture(scope="session")
def ros2_init():
    rclpy.init()
    yield
    rclpy.shutdown()

@pytest.fixture(scope="module")
def sensor_data_publisher(ros2_init):
    node = SensorDataPublisher()
    yield node
    node.destroy_node()

@pytest.fixture(scope="module")
def sensor_data_validator(ros2_init):
    node = SensorDataValidator()
    yield node
    node.destroy_node()