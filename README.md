# ROS 2 Validation Suite
------------------------

## Objective
- A ROS 2 system for IMU sensor validation with an autoamted test suite and CI/CD pipeline

## Architecture
```
sensor_data_publisher.py => publish topic/imu_data
sensor_data_publisher.py => subscribe to topic /imu_data, publish topic /imu_diag
sensor_data_alert.py => subscribe to topic /imu_diag
```

## Folder / File Structure
```
root/
|---src/validation_suite/ # ROS 2 package directory
|       |---scripts/ # directory containing publisher, validator, and alert nodes
|---tests/ # directory containing automated test suite

## CI / CD
- On each commit & daily schedule (10 AM PST), action will run pytest suite
