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
- On each commit & daily schedule (10 AM PST), automated QA test suite is ran

## Screenshots

**Observability Platform**

----------------------
<img width="1521" height="713" alt="Screenshot 2026-07-22 121500" src="https://github.com/user-attachments/assets/5e3f926b-4f23-42f8-ad68-057f8c485353" />
<img width="1499" height="328" alt="Screenshot 2026-07-22 121513" src="https://github.com/user-attachments/assets/ebde54e7-a2fa-4e1e-b731-deec7418adce" />

----------------------

**QA Automation Suite**

----------------------

<img width="1514" height="427" alt="Screenshot 2026-07-21 001930" src="https://github.com/user-attachments/assets/4c860d05-c9a0-4c4b-a8b4-99a437d701a4" />
<img width="1498" height="670" alt="Screenshot 2026-07-21 001946" src="https://github.com/user-attachments/assets/dc84bf90-36cf-4f95-8bed-5ea28d827aef" />

----------------------
