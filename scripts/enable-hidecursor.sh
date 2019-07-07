#!/bin/bash

su $2 -c "echo \"[Desktop Entry]\" > $1"
su $2 -c "echo \"Type=Application\" >> $1"
su $2 -c "echo \"Name=Unclutter\" >> $1"
su $2 -c "echo \"Exec=unclutter -jitter 100\" >> $1"