# ROS 2 Observability Platform & QA Automation Suite
------------------------
**[Link to Observability Platform Dashboard](https://quirkywisteria3067.grafana.net/public-dashboards/74148b07187b4af7a8eaaa73b7b13a43)**

**[Link to CI & QA Test Suite Dashboard](https://quirkywisteria3067.grafana.net/public-dashboards/e93bbf96b5fc46ef8d552fda9c8f8b34)**

## Objective
A combination of two main projects:
- A simulated ROS 2 System that continously publishes metrics for IMU, Odometry, and BatteryState data
- An automated QA test suite to validate node availability, topic messages, and publisher/subscriber connectivity
  
## Architecture
- On the Linux VM system, ROS 2 & Prometheus nodes are kept continuously running via `systemd service .service files`
<img width="1226" height="709" alt="image" src="https://github.com/user-attachments/assets/0608cbab-21ec-4704-bf78-15f88362b598" />

## CI / CD
- On each commit & daily schedule (3x/day), QA automation suite is ran

## Screenshots

**Observability Platform**

----------------------

<img width="1525" height="797" alt="Screenshot 2026-07-19 210937" src="https://github.com/user-attachments/assets/46c43bda-eb06-4aae-a74e-86384ce3ce20" />
<img width="1524" height="488" alt="Screenshot 2026-07-19 210949" src="https://github.com/user-attachments/assets/2f7f4a68-e606-4c64-8ac3-791d89e3671b" />

----------------------

**QA Automation Suite**

----------------------

<img width="1521" height="713" alt="Screenshot 2026-07-22 121500" src="https://github.com/user-attachments/assets/aacff137-1552-4836-b09c-c5dfab0a8176" />
<img width="1499" height="328" alt="Screenshot 2026-07-22 121513" src="https://github.com/user-attachments/assets/8da75a38-c6f2-489e-a6eb-c97917ec60ad" />

----------------------
