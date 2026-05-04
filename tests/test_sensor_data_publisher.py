import pytest
import math
import transforms3d
from config import IMU_RANGES
from rclpy.time import Time

class TestSensorDataPublishser:

    def test_generate_imu_header(sensor_data_publisher):
        '''
        Test function for generate_imu_header

        Fixture(s):
            - sensor_data_publisher: Initialize SensorDataPublisher with module scope
        '''
        imu_header_data = sensor_data_publisher.generate_imu_header()
        
        assert Time.from_msg(imu_header_data.stamp) != Time()
        assert imu_header_data.frame_id == "imu_link"
    
    @pytest.mark.parametrize("quality_level", ["good", "warn", "poor"])
    def test_orientation(sensor_data_publisher, quality_level):
        '''
        Test function for generate_imu_header

        Fixture(s):
            - sensor_data_pulisher: Continues using same SensorDataPublisher with module scope
        '''
        angular_velocity_data = sensor_data_publisher.generate_orientation(quality_level)
        w = angular_velocity_data.w
        x = angular_velocity_data.x
        y = angular_velocity_data.y
        z = angular_velocity_data.z

        roll_rads, pitch_rads, yaw_rads = transforms3d.euler.quat2euler([w, x, y, z], axes='sxyz')

        roll_deg = math.degrees(roll_rads)
        pitch_deg = math.degrees(pitch_rads)
        yaw_deg = math.degrees(yaw_rads)
