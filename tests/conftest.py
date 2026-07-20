import sys
import os
import pytest
import rclpy
import yaml

sys.path.append(os.path.join(os.path.dirname(__file__), '../src/validation_suite/scripts'))

from config import IMU_RANGES
from rclpy.node import Node

@pytest.fixture(scope="session")
def ros2_init():
    rclpy.init()
    yield
    rclpy.shutdown()

@pytest.fixture(scope="module")
def node_list_node(ros2_init):
    node = Node('discovery_node')
    yield node
    node.destroy_node()

@pytest.fixture(scope="module")
def config_load():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(base_dir)
    def _loader(filename):
        path = os.path.join(base_dir, f"./configs/{filename}")
        with open(path, 'r') as f:
          return yaml.load(f, Loader=yaml.SafeLoader)
    return _loader