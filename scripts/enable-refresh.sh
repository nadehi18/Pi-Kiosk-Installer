#!/bin/bash



su $2 -c "echo \"#!/bin/bash\" > $1"
su $2 -c "echo \"DISPLAY=:0 xdotool getactivewindow key F5\" >> $1"

su $2 -c "chmod +x $1"
