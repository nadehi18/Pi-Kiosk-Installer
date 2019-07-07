#!/bin/bash

# This script adds a cron job without deleting previous items.
# It takes the user of the cron job as the first argument,
# and the file containing the text to append as the second argument.
# The interval in minutes for the cron job as the third argument.
# And the filename of the script as the fourth argument.

su $1 -c "install -Dv /dev/null $2"

declare -i a=1

if [ $3 -gt $a ]; then
    su $1 -c "echo \"*/$3 * * * *  $4\" > $2" 
else
    su $1 -c "echo \"* * * * *  $4\" > $2"
fi


crontab -l -u $1 | cat - $2 | crontab -u $1 -