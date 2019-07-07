#!/usr/bin/env python

import os
import subprocess
import apt

class Setup():
    def __init__(self, cli):

        if cli:
            print("Welcome to the Raspberry Pi Kiosk Creation Tool!")
            print("If you do not wish to enable a feature, just leave the prompt blank and press [ENTER].")
        
            # Get the url of the presentation
            self.presentation_url = input("Please enter the url of the presentation to use for the kiosk: ")
        
            # Can't auto start the kiosk if there is no powerpoint
            if self.presentation_url:
                self.user_autostart = input("Please enter the user to enable auto start of the kiosk for: ")
            # Set the auto start and refresh features to off
            else:
                self.user_autostart = ""

            if self.user_autostart:
                self.auto_start(self.user_autostart, self.presentation_url)

            # Get the auto refresh interval in minutes.
            self.refresh_interval = input("Please enter the interval in minutes that you want the kiosk to refresh the Google Slides presentation: ")
            
            if self.refresh_interval:
                    self.refresh(self.refresh_interval, self.user_autostart)
        
            # Get the user for autologin        
            self.user_autologin = input("Please enter the user to enable auto login for: ")

            if self.user_autologin:
                self.auto_login(self.user_autologin)

            # Get user choice for auto updates
            self.choice_autoupdate = input("Would you like to enable automatic updates? (y/n) ")

            if self.choice_autoupdate and not "n" in self.choice_autoupdate and not "N" in self.choice_autoupdate:
                self.auto_update()

            print("The Creation Tool is finished.  Please restart to enable your selected features.")

    # This function makes the kiosk start automatically at user login
    def auto_start(self, user, url):

        directory = "/home/" + user + "/.config/autostart"
        filename = directory + "/kiosk.desktop"
        opened = False
    
        if not os.path.exists(directory):
            os.makedirs(directory)
    
        # Creates a desktop file in the autostart dir to run the kiosk automatically
        # Checks if the default filename exists and if it does, the program 
        while not opened:
            if not os.path.isfile(filename):
                desktop_file = open(filename, "w")
                opened = True
            else:
                filename = directory + "/" + input("ERROR: File " + filename + "exists.  Please enter new filename: ") + ".desktop"
        desktop_file.close()

        if user == os.getenv("USER"):
             subprocess.call([os.path.dirname(os.path.realpath("__file__")) + "/scripts/enable-autostart.sh", filename, url, user])
        else:    
            subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/scripts/enable-autostart.sh", filename, url, user])

    
    # This function makes the selected user auto login.
    # It calls a shell script and enables it to run with root privileges.
    def auto_login(self, user):
        subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/scripts/enable-autologin.sh", user])

    # This function enables automatic updates.
    # It calls a shell script and enables it to run with root privileges.
    def auto_update(self):
        self.ensure_package_installed("unattended-upgrades")
        
        subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/scripts/enable-autoupdates.sh"])

    # This function adds a cronjob that refreshes the kiosk every so many minutes.
    # It requires root privileges to actually update the selected users crontab.
    def refresh(self, interval, user):
        self.ensure_package_installed("xdotool")
        
        directory = "/home/" + user
        filename =  directory + "/.refresh-kiosk.sh"
        opened = False

        while not opened:
            if not os.path.isfile(filename):
                refresh_file = open(filename, "w")
                opened = True
            else:
                filename = directory + "/." + input("ERROR: File " + filename + "exists.  Please enter new filename: ") + ".sh"
        refresh_file.close()

        if user == os.getenv("USER"):
             subprocess.call([os.path.dirname(os.path.realpath("__file__")) + "//scriptsenable-refresh.sh", filename, user])
        else:    
            subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "//scriptsenable-refresh.sh", filename, user])
        
        refresh_filename = filename

        opened = False
        filename =  directory + "/.cronkiosk"

        while not opened:
            if not os.path.isfile(filename):
                cron_file = open(filename, "w")
                opened = True
            else:
                filename = directory + "/." + input("ERROR: File " + filename + " exists.  Please enter new filename: ")
        cron_file.close()

        subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/scripts/install-crontab.sh", user, filename, int(interval), refresh_filename])

        os.remove(filename)

    def ensure_package_installed(self, package_name):
        cache = apt.Cache()
        package = cache[package_name]
        if not package.is_installed:
            print("The " + package_name + "package is not installed.  Installing now...")
            subprocess.call(["pkexec", "apt", "update", "&&", "apt", "install", package-name, "-y"])

if __name__ == '__main__':
    Setup(True)
    


