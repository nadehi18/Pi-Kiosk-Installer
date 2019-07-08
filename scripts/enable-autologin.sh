#!/bin/bash

# This script enables auto login on Raspbian (Or any Linux distro that uses LightDM).
# It takes the name of the user to auto login to as an argument. 
# This script must be run as root or else it will not work at all.

# The script inserts "autologin-user=specified_user" directly under the line that contains [Seat:*].
# The script also removes any other autologin-user line to prevent conflicts.
# Lastly the script reconfigures LightDM to enable the auto login.


match="\[Seat\:\*\]"
insert="autologin-user=$1"
file="/etc/lightdm/lightdm.conf"
sed -i "/autologin-user/d" $file
sed -i "s/^$match/$match\n$insert/" $file
dpkg-reconfigure lightdm 