#!/bin/bash

# This script adds a cron job without deleting previous items.
# It takes the user of the cron job as the first argument,
# and the file containing the text to append as the second argument.

crontab -l -u $1 | cat - $2 | crontab -u $1 -