#!/bin/bash

# install a sysctl service that will 'roslaunch vehicle_monitor bringup.launch' on boot
# this includes sourceing the ROS environment on startup and executin the launch file

# create the service file from the template in this directory
cp vehicle_monitor.service /etc/systemd/system/

# reload the systemd daemon to include the new service
systemctl daemon-reload

# enable the service to run on boot
systemctl enable vehicle_monitor.service

# start the service
systemctl start vehicle_monitor.service

# check the status of the service
systemctl status vehicle_monitor.service

# echo a sucessful message telling the user to reboot to test!
echo "Vehicle Monitor service installed and started. Reboot to test!"snip