import sys
import os
import pytest
from rclpy.node import Node
from sensor_data_publisher import SensorDataPublisher
from sensor_data_validator import SensorDataValidator
from sensor_data_alert import SensorDataAlert

sys.path.append(os.path.join(os.path.dirname(__file__), '../src/validation_suite/scripts'))

@pytest.fixture()
def sensor_data_publisher():
    rclpy.init()
    node = SensorDataPublisher()
    yield node
    node.destroy_node()
    rclpy.shutdown()

@pytest.fixture()
def sensor_data_validator():
    rclpy.init()
    node = SensorDataValidator()
    yield node
    node.destroy_node()
    rclpy.shutdown()
