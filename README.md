STINGRAY / CORVETTE 

taking wheel position data along with IMU data to analyze the C.O.B and dynamics of a corvette stingray during a race

# References

- [flashing arduino over raspi](https://siytek.com/arduino-cli-raspberry-pi/#Configure-Arduino)
- [BOM](https://docs.google.com/spreadsheets/d/15MNyfEw0GuSBbplbCHpf8V5PrWQOQE57q0T67NCtYUg/edit?usp=sharing)
- [IMU driver cpp sample code](https://github.com/ZFDD96/BWT61CL/blob/master/Sample%20Code.zip)
- [uploading to arduino over raspi](https://github.com/guysoft/OctoPi/issues/23)
- [lauching ros program on bootup](https://roboticsbackend.com/make-a-raspberry-pi-3-program-start-on-boot/)

# System Overview

- Ubuntu 20.04 running on an [Intel NUC based PC](https://www.intel.com/content/www/us/en/products/docs/boards-kits/nuc/overview.html)
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
- [x] full bringup test (multiple reboots)
- [x] test full system w/ data collect
- [ ] easy to use UI / HMI (display??)
- [ ] wiring diagram
- [ ] data analysis code work


2/2/24: 
We've decided to swap to an x86 based computer that will still run Ubuntu 20.04. The reason for the switch was for more reliablity and ease of use. The Raspberry Pi 4 Rasbian OS nor Ubuntu 20.04 run very well with ROS noetic, which is the version we are using. The x86 computer will be a more reliable and faster option for our project. Plus we didn't use very many GPIO and most of them were for digital I/O which we can easily replicate with the arduino. The arduino is currenty an Uno Rev3, however we can swap it out if more performance is needed. Its basically a digital I/O board for the sensors and switches. 