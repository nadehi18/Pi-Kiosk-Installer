#!/bin/bash

su $3

echo "[Desktop Entry]" > $1
echo "Type=Application" >> $1
echo "Name=Kiosk" >> $1
echo "Exec=chromium-browser --kiosk $2" >> $1

exit