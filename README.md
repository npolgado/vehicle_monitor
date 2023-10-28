STINGRAY

taking wheel position and pressure data along with IMU data to analyze the C.O.B and dynamics of a corvette stingray

# References

- [flashing arduino over raspi](https://siytek.com/arduino-cli-raspberry-pi/#Configure-Arduino)
- [BOM](https://docs.google.com/spreadsheets/d/15MNyfEw0GuSBbplbCHpf8V5PrWQOQE57q0T67NCtYUg/edit?usp=sharing)
- [IMU driver cpp sample code](https://github.com/ZFDD96/BWT61CL/blob/master/Sample%20Code.zip)
- [uploading to arduino over raspi](https://github.com/guysoft/OctoPi/issues/23)

# System Overview

- Ubuntu 20.04 Server Arm64 running on a Raspberry Pi 4 (4GB)
- 4 Rideheight Position sensors along each wheel of the vehicle
- USB 3.0 IMU with magnometer and heading based filtered imu data @ 100 hz
- Arduino Uno Rev3 connected over USB 3.0

#TO DO:

- [x] ADC code for data aquistion
- [x] Read/Write speed test and data throughput estimation
- [x] serial communication for ADC (OR through USB??)
- [x] data recording scheme (cvs? txt?)
- [x] Parse IMU data (Inertial Sense or LORD)
- [x] benchmark data throughput
- [x] ROS bringup launch file
- [x] Arduino Ros Driver
- [ ] full bringup test (multiple reboots)
- [ ] test full system w/ data collect
- [ ] easy to use UI / HMI (display??)
- [ ] wiring diagram
- [ ] data analysis code work
