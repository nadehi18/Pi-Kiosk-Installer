#!/bin/bash

# This script enables auto login on Raspbian (Or any linux distro that uses lightdm).
# It takes the name of the user to auto login to as an argument. 
# This script MUST be run as root or else it will not work, at all.


match="[LightDM]"
insert="autologin-user=$1\nautologin-user-timeout=0"

sed -i "s/$match/$match\n$insert/" /etc/lightdm/lightdm.conf
dpkg-reconfigure lightdm 