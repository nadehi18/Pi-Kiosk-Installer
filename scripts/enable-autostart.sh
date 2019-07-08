#!/bin/bash

# This script creates a .desktop file for the kiosk for the specified URL to the specified location as a specified user.
# This script needs to be run as root to avoid the user being prompted for a password for every su command.

su $3 -c "install -Dv /dev/null $1"

su $3 -c "echo \"[Desktop Entry]\" > $1"
su $3 -c "echo \"Type=Application\" >> $1"
su $3 -c "echo \"Name=Kiosk\" >> $1"
su $3 -c "echo \"Exec=chromium-browser --kiosk $2\" >> $1"


