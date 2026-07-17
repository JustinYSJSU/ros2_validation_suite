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
<img width="1827" height="839" alt="image" src="https://github.com/user-attachments/assets/5997864a-1f68-4b14-90b2-a8bda4a7b500" />
<img width="1827" height="250" alt="image" src="https://github.com/user-attachments/assets/6a3f752b-ccbb-4b45-80d8-1c0ac027e7a3" />
