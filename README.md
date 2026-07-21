# ROS 2 Observability Platform & QA Automation Suite
------------------------
**[Link to Observability Platform](https://quirkywisteria3067.grafana.net/public-dashboards/74148b07187b4af7a8eaaa73b7b13a43)**
**[Link to CI & QA Test Suite](https://quirkywisteria3067.grafana.net/public-dashboards/e93bbf96b5fc46ef8d552fda9c8f8b34)**

## Objective
A combination of two main projects:
- A simulated ROS 2 System that continously publishes metrics for IMU, Odometry, and BatteryState data
- An automated QA test suite to validation node availability, topic messages, and publisher/subscriber connectivity
  
## Architecture
- On the Linux VM system, ROS 2 & Prometheus nodes are kept continuously running via `systemd service .service files`
<img width="1226" height="709" alt="image" src="https://github.com/user-attachments/assets/0608cbab-21ec-4704-bf78-15f88362b598" />

## CI / CD
- On each commit & daily schedule (10 AM PST), automated QA test suite is ran

## Screenshots

**Observability Platform**

----------------------

<img width="1525" height="797" alt="Screenshot 2026-07-19 210937" src="https://github.com/user-attachments/assets/a8552bdd-2e25-41f3-9ea9-b106283687d4" />
<img width="1524" height="488" alt="Screenshot 2026-07-19 210949" src="https://github.com/user-attachments/assets/a53ab6c9-b9e8-4fdb-a48b-4a3c13ba3bdf" />

----------------------
