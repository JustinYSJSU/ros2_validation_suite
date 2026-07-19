#!/usr/bin/python3

"""battery_publisher.py

Generates simulated battery data and publishes to the 'battery_data' topic at 5.0s intervals.
"""
import random
import rclpy
import transforms3d
import math
import config
from rclpy.node import Node
from std_msgs.msg import Header
from sensor_msgs.msg import BatteryState

CHARGE_THRESHOLD = 0.5
MIN_VOLTAGE = 9.0
MAX_VOLTAGE = 12.0

class BatteryNode(Node):
    """Publishes simulated battery data and publishes to
    'battery_data' topic

        Topics:
            /battery_data
    """
    
    def __init__(self):
        super().__init__("battery_publisher")
        self.pub = self.create_publisher(BatteryState, "battery_data", 10)
        self.timer = self.create_timer(5.0, self.battery_callback)

        self.battery_percentage = 1.0
        self.discharge_rate = 0.01
        self.charge_rate = 0.02
        self.voltage = MIN_VOLTAGE + (MAX_VOLTAGE - MIN_VOLTAGE) * self.battery_percentage

        self.is_charging = False

    def battery_callback(self):
        """Performs battery discharge / charging and publishes
        BatteryState message to reflect current battery status

        Topics:
            /battery_data
        """
        msg = BatteryState()

        head = Header()
        head.stamp = self.get_clock().now().to_msg()
        head.frame_id = "battery_link"

        self.check_charge()
        
        if self.is_charging:
            self.battery_percentage += self.charge_rate
            self.voltage = MIN_VOLTAGE + (MAX_VOLTAGE - MIN_VOLTAGE) * self.battery_percentage
        else:
            self.battery_percentage -= self.discharge_rate
            self.voltage = MIN_VOLTAGE + (MAX_VOLTAGE - MIN_VOLTAGE) * self.battery_percentage

        msg.percentage = self.battery_percentage
        msg.voltage = self.voltage
        msg.header = head
        self.pub.publish(msg)
    
    def check_charge(self):
        """Checks current battery charge, begin charging if <0.5 (50%)

        Topics:
            /battery_data
        """
        if self.battery_percentage >= 1.0:
            self.is_charging = False
            self.battery_percentage = 1.0
            self.voltage = MAX_VOLTAGE
        elif self.battery_percentage <= CHARGE_THRESHOLD:
            self.is_charging = True
