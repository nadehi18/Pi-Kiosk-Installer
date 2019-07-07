#!/bin/bash

# This script enables auto updates using the unattended-upgrades package which should be installed by default

echo unattended-upgrades unattended-upgrades/enable_auto_updates boolean true | debconf-set-selections
dpkg-reconfigure -f noninteractive unattended-upgrades