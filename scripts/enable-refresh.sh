#!/bin/bash

# This script creates a shell script at the specified path that emulates a F5 keypress using the package xdotool.
# This script needs to be run as root to avoid the user being prompted for a password for every su command.

su $2 -c "install -Dv /dev/null $1"

su $2 -c "echo \"#!/bin/bash\" > $1"
su $2 -c "echo \"DISPLAY=:0 xdotool getactivewindow key F5\" >> $1"

su $2 -c "chmod +x $1"
