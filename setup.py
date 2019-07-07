#!/usr/bin/env python

import os
import subprocess

class Setup():
    def __init__(self):

        # Get the url of the presentation
        self.presentation_url = input("Please enter the url of the presentation to use for the kiosk: ")
        
        # Can't auto start or refresh the kiosk if there is no powerpoint
        if self.presentation_url:
            self.user_autostart = input("Please enter the user to enable auto start of the kiosk for: ")
            self.refresh_interval = input("Please enter the interval in minutes that you want the kiosk to refresh the Google Slides presentation: ")
        # Set the auto start and refresh features to off
        else:
            self.user_autostart = ""
            self.refresh_interval = ""

        # Get the user for autologin        
        self.user_autologin = input("Please enter the user to enable auto login for: ")

        # Get user choice for auto updates
        self.choice_autoupdate = input("Would you like to enable automatic updates? (y/n) ")

        if self.user_autostart:
            self.autostart(self.user_autostart, self.presentation_url)
            if self.refresh_interval:
                self.refresh(self.refresh_interval, self.user_autostart)
        
        if self.user_autologin:
            self.autologin(self.user_autologin)
        
        if self.choice_autoupdate and not "n" in self.choice_autoupdate and not "N" in self.choice_autoupdate:
            self.autoupdate()



        print("The Creation Tool is finished.  Please restart to enable your selected features.")

    # This function makes the kiosk start automatically at user login
    def autostart(self, user, url):

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
    
        desktop_file.write("[Desktop Entry]" + '\n')
        desktop_file.write("Type=Application" + '\n')
        desktop_file.write("Name=Kiosk" + '\n')
        desktop_file.write("Exec=chromium-browser --kiosk " + url)
        desktop_file.close()
    
    # This function makes the selected user auto login.
    # It calls a shell script and enables it to run with root privileges.
    def autologin(self, user):
        subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/enable-autologin.sh", user])

    # This function enables automatic updates.
    # It calls a shell script and enables it to run with root privileges.
    def autoupdate(self):
        subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/enable-autoupdates.sh"])

    # This function adds a cronjob that refreshes the kiosk every so many minutes.
    # It requires root privileges to actually update the selected users crontab.
    def refresh(self, interval, user):
        directory = "/home/" + user
        filename =  directory + "/.refresh-kiosk.sh"
        opened = False

        while not opened:
            if not os.path.isfile(filename):
                refresh_file = open(filename, "w")
                opened = True
            else:
                filename = directory + "/." + input("ERROR: File " + filename + "exists.  Please enter new filename: ") + ".sh"

        refresh_file.write("#!/bin/bash"  + '\n')
        refresh_file.write("DISPLAY=:0 xdotool getactivewindow key F5")
        refresh_file.close()

        subprocess.Popen(['chmod', "+x", filename])
        
        refresh_filename = filename

        opened = False
        filename =  directory + "/.cronkiosk"

        while not opened:
            if not os.path.isfile(filename):
                cron_file = open(filename, "w")
                opened = True
            else:
                filename = directory + "/." + input("ERROR: File " + filename + " exists.  Please enter new filename: ")

        if int(interval) > 1:
            cron_file.write("*/" + str(interval) + " * * * *  " + refresh_filename + '\n')
        else:
            cron_file.write("* * * * *  " + refresh_filename + '\n')
        cron_file.close()

        subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/install-crontab.sh", user, filename])

        os.remove(filename)

print("Welcome to the Raspberry Pi Kiosk Creation Tool!")
print("If you do not wish to enable a feature, just leave the prompt blank and press [ENTER].")

if __name__ == '__main__':
    Setup()
    


