#!/bin/bash

su $2

echo "#!/bin/bash" > $1
echo "DISPLAY=:0 xdotool getactivewindow key F5" >> $1

chmod +x $1

exit