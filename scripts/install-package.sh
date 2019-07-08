#!/bin/bash

# This script installs a specified package via apt.
# Needs to be run as root or it will not work at all.

apt update 
apt install $1 -y