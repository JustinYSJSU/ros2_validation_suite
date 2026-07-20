# ROS 2 System Monitoring
------------------------
**[Link to live dashboard](https://quirkywisteria3067.grafana.net/public-dashboards/74148b07187b4af7a8eaaa73b7b13a43)**

## Objective
- A ROS 2 system for IMU sensor validation with an autoamted test suite, CI/CD pipeline, and live data viusalization
  
## Architecture
- On the Linux VM system, ROS 2 & Prometheus nodes are kept continuously running via `systemd service .service files`
<img width="1228" height="728" alt="image" src="https://github.com/user-attachments/assets/5169d31c-305f-4103-ad70-0bf1488a5bda" />


## CI / CD
- On each commit & daily schedule (10 AM PST), action will run pytest suite

## Screenshots
<img width="1533" height="758" alt="Screenshot 2026-07-19 201327" src="https://github.com/user-attachments/assets/2703f02d-dce1-4a28-9782-551c8c24efe7" />
<img width="1529" height="802" alt="image" src="https://github.com/user-attachments/assets/5ce7c05b-5a43-45bf-9ce9-f1dd4d051e11" />

