import pytest
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