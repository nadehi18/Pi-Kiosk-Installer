#!/bin/bash

# This script creates a .desktop file for the unclutter package to the specified location as a specified user.
# This script needs to be run as root to avoid the user being prompted for a password for every su command.

su $2 -c "install -Dv /dev/null $1"
su $2 -c "echo \"[Desktop Entry]\" > $1"
su $2 -c "echo \"Type=Application\" >> $1"
su $2 -c "echo \"Name=Unclutter\" >> $1"
su $2 -c "echo \"Exec=unclutter -jitter 100\" >> $1"