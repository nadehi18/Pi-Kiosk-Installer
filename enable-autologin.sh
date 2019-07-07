#!/bin/bash

# This script enables auto login on Raspbian (Or any linux distro that uses lightdm).
# It takes the name of the user to auto login to as an argument. 
# This script MUST be run as root or else it will not work, at all.

echo autologin-user=$1 >> /etc/lightdm/lightdm.conf
echo autologin-user-timeout=0 >> /etc/lightdm/lightdm.conf
dpkg-reconfigure lightdm 