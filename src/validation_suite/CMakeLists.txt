cmake_minimum_required(VERSION 3.8)
project(validation_suite)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(diagnostic_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

ament_python_install_package(scripts)


rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/TelemetryBatteryState.msg"
  "msg/TelemetryImu.msg"
  "msg/TelemetryOdometry.msg"
  DEPENDENCIES std_msgs
)

install(PROGRAMS
  scripts/imu_publisher.py
  scripts/odometry_publisher.py
  scripts/prom_exporter.py
  scripts/battery_publisher.py
  scripts/telemetry_imu_collector.py
  DESTINATION lib/${PROJECT_NAME}
)

install(FILES
  scripts/config.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_dependencies(rosidl_default_runtime)

ament_package()
