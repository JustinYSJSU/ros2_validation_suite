import pytest
import math
import transforms3d
from config import IMU_RANGES
from rclpy.time import Time
from rclpy.clock import ClockType

from std_msgs.msg import Header
from geometry_msgs.msg import Quaternion # orientation
from geometry_msgs.msg import Vector3 # angular_velocity + linear acceleration

class TestSensorDataValidator():

    @pytest.mark.parametrize("time_valid, frame_id, valid_result", [(True, "imu_link", True),
    (False, "imu_link", False), (True, "not_imu", False), (False, "not_imu", False)])
    def test_validate_imu_header(self, sensor_data_validator, time_valid, frame_id, valid_result):
        """
        Test function validate_imu_header

        Fixture(s):
            - sensor_data_validator: Using sensor_data_validator fixture with module scope
        """
        head = Header()
        if time_valid:
            head.stamp = sensor_data_validator.get_clock().now().to_msg()
        else:
            head.stamp = Time().to_msg()
        head.frame_id = frame_id

        assert sensor_data_validator.validate_imu_header(head) == valid_result

    @pytest.mark.parametrize("w, x, y, z, expected", [
    (1.0,    0.0,    0.0, 0.0, "good"),   
    (0.9659, 0.2588, 0.0, 0.0, "warn"),  
    (0.7071, 0.7071, 0.0, 0.0, "poor"),
    (1.0,    1.0,    0.0, 0.0, "poor"),
    ])
    def test_validate_imu_orientation(self, sensor_data_validator, w, x, y, z, expected):
        """
        Test function validate_imu_orientation

        Fixture(s):
            - sensor_data_validator: Using sensor_data_validator fixture with module scope
        """
        quat = Quaternion()
        quat.w = w
        quat.x = x
        quat.y = y
        quat.z = z

        assert sensor_data_validator.validate_imu_orientation(quat) == expected