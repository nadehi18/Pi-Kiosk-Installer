#!/bin/bash

su $3 -c "echo \"[Desktop Entry]\" > $1"
su $3 -c "echo \"Type=Application\" >> $1"
su $3 -c "echo \"Name=Kiosk\" >> $1"
su $3 -c "echo \"Exec=chromium-browser --kiosk $2\" >> $1"


