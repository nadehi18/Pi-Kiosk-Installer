#!/bin/bash

# This script enables auto login on Raspbian (Or any linux distro that uses lightdm).
# It takes the name of the user to auto login to as an argument. 
# This script MUST be run as root or else it will not work, at all.


match="\[Seat\:\*\]"
insert="autologin-user=$1"
file="/etc/lightdm/lightdm.conf"
sed -i "/autologin-user/d" $file
sed "s/<$match>/<$match>\n$insert/" $file
dpkg-reconfigure lightdm 