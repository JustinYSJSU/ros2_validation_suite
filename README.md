# ROS 2 System Monitoring
------------------------
**[Link to live dashboard](https://quirkywisteria3067.grafana.net/public-dashboards/74148b07187b4af7a8eaaa73b7b13a43)**

## Objective
- A ROS 2 system for IMU sensor validation with an autoamted test suite, CI/CD pipeline, and live data viusalization
  
## Architecture
- On the Linux VM system, ROS 2 & Prometheus nodes are kept continuously running via `systemd service .service files`
<img width="992" height="464" alt="image" src="https://github.com/user-attachments/assets/45dd6c26-1818-46ff-b3a0-3f4a4d307ab0" />

## CI / CD
- On each commit & daily schedule (10 AM PST), action will run pytest suite

## Screenshots
<img width="1533" height="758" alt="Screenshot 2026-07-19 201327" src="https://github.com/user-attachments/assets/2703f02d-dce1-4a28-9782-551c8c24efe7" />
<img width="1532" height="788" alt="Screenshot 2026-07-19 201407" src="https://github.com/user-attachments/assets/3eceef4d-90e6-448b-b02d-b8038999b51a" />
