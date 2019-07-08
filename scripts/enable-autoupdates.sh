#!/bin/bash

# This script enables auto updates using the unattended-upgrades package which should be installed by default
# Most of this is probably done automatically when the package is installed, but this is done just in case.

echo unattended-upgrades unattended-upgrades/enable_auto_updates boolean true | debconf-set-selections
dpkg-reconfigure -f noninteractive unattended-upgrades