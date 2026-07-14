# ROS 2 Validation Suite
------------------------
**[Link to live dashboard](https://quirkywisteria3067.grafana.net/public-dashboards/74148b07187b4af7a8eaaa73b7b13a43)**

## Objective
- A ROS 2 system for IMU sensor validation with an autoamted test suite and CI/CD pipeline
- System runs on a Linux virtual machine (VM) hosted via Google Cloud.
- System metrics are scaped & exposed via Prometheus, and displayed on Grafana for viewing

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
```

## CI / CD
- On each commit & daily schedule (10 AM PST), action will run pytest suite
