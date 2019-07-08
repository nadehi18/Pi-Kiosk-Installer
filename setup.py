#!/usr/bin/env python3

# Import libraries
import os
import subprocess
import apt

# The main class containing all of the installation methods
class Setup():
    def __init__(self, cli):

        # There only needs to be initialization if the installer is being run in the console
        if cli:

            # Declare the divider decoration
            self.divider = '-' * 40

            print('\n' + self.divider + '\n')

            # Print the welcome message
            print("Welcome to the Raspberry Pi Kiosk Creation Tool!")
            print("If you do not wish to enable a feature, just leave the prompt blank and press [ENTER].")
        
            print('\n' + self.divider + '\n')

            # Get the url of the presentation
            self.presentation_url = input("Please enter the url of the website to use for the kiosk: ")
        
            # Can't auto start the kiosk if there is no powerpoint
            if self.presentation_url:
                self.user_autostart = input("Please enter the user to enable auto start of the kiosk for: ")
            # Set the auto start feature to off
            else:
                self.user_autostart = ""
    
            # Execute the autostart function if it is needed
            if self.user_autostart:
                self.auto_start(self.user_autostart, self.presentation_url)

            print('\n' + self.divider + '\n')
            
            # Get the auto refresh interval in minutes.
            self.refresh_interval = input("Please enter the interval in minutes that you want the kiosk to refresh: ")
            
            # Execute the refresh function if it is needed
            if self.refresh_interval:
                    self.refresh(self.refresh_interval, self.user_autostart)

            print('\n' + self.divider + '\n')

            # Get the user to hide the cursor for.
            self.auto_hide_user = input("Please enter the user to automatically hide the cursor for: ")
            
             # Execute the autohide function if it is needed
            if self.auto_hide_user:
                    self.auto_hide_mouse(self.auto_hide_user)

            print('\n' + self.divider + '\n')    
            
            # Get the user for autologin        
            self.user_autologin = input("Please enter the user to enable auto login for: ")

             # Execute the autologin function if it is needed
            if self.user_autologin:
                self.auto_login(self.user_autologin)
            
            print('\n' + self.divider + '\n')
            
            # Get user choice for auto updates
            self.choice_autoupdate = input("Would you like to enable automatic updates? (y/n) ")

             # Execute the autoupdate function if it is needed
            if self.choice_autoupdate and not "n" in self.choice_autoupdate and not "N" in self.choice_autoupdate:
                self.auto_update()
            
            print('\n' + self.divider + '\n')
            
            # Print the ending message
            print("The Creation Tool is finished.  Please restart to enable your selected features.")

            print('\n' + self.divider + '\n')

    # This function makes the kiosk start automatically at user login
    def auto_start(self, user, url):

        extension = ".desktop"
        directory = "/home/" + user + "/.config/autostart/"
        filename = directory + "kiosk" + extension
        
        filename = self.check_file_exists(filename, directory, extension)

        subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/scripts/enable-autostart.sh", filename, url, user])

    
    # This function makes the selected user auto login.
    # It calls a shell script and enables it to run with root privileges.
    def auto_login(self, user):
        subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/scripts/enable-autologin.sh", user])

    # This function enables automatic updates.
    # It calls a shell script and enables it to run with root privileges.
    def auto_update(self):
        # Make sure the needed package is installed.
        self.ensure_package_installed("unattended-upgrades")
        
        # Run an elevated shell script.
        subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/scripts/enable-autoupdates.sh"])

    # This function adds a cronjob that refreshes the kiosk every so many minutes.
    # It requires root privileges to actually update the selected users crontab.
    def refresh(self, interval, user):
        # Make sure the needed package is installed.
        self.ensure_package_installed("xdotool")
        
        # Set the variables for the function
        extension = ".sh"
        directory = "/home/" + user + "/"
        refresh_filename = directory + ".refresh-kiosk" + extension
        filename = directory + ".cronkiosk" + extension
        
        # Make sure it is safe to create the file
        refresh_filename = self.check_file_exists(refresh_filename, directory, extension)

        # Call an elevated shell to create the script as the specified user.
        subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/scripts/enable-refresh.sh", filename, user])
        
        # Make sure it is safe to create the file; the third argument is blank because there is no extension.
        filename = self.check_file_exists(filename, directory, "")

        # Call an elevated shell to install the script as the specified user.
        subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/scripts/install-crontab.sh", user, filename, str(interval), refresh_filename])

        # Remove the extra file if possible
        try:
            os.remove(filename)

    # This function uses the unclutter package to make the cursor invisible when not in use.
    # It makes a .desktop file in the user's autostart directory.
    def auto_hide_mouse(self, user):
        # Make sure the needed package is installed.
        self.ensure_package_installed("unclutter")

        # Set the variables for the function
        extension = ".desktop"
        directory = "/home/" + user + "/.config/autostart/"
        filename = directory + "unclutter" + extension

        # Make sure it is safe to create the file
        filename = self.check_file_exists(filename, directory, extension)

        # Call an elevated shell to create the file as the specified user.
        subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/scripts/enable-hidecursor.sh", filename, user])

    # This function makes sure a package is installed using apt.
    # If the package is not installed, the function installs it
    def ensure_package_installed(self, package_name):
        # Get the installed package cache
        cache = apt.Cache()
        # Select the package from the cache
        package = cache[package_name]
        # Only do something if the package is not installed
        if not package.is_installed:
            print('\n' + self.divider + '\n')
            # Alert the user that the installer will attempt to install the package.
            print("The " + package_name + " package is not installed.  Installing now...")
            # Call an elevated shell that will run the installer script.
            subprocess.call(["pkexec", os.path.dirname(os.path.realpath("__file__")) + "/scripts/install-package.sh", package_name])
            print('\n' + self.divider + '\n')
    
    # This function checks if a file exists, and if it does, it prompts the user to replace or rename the file.
    # The function returns the filename with full path.
    def check_file_exists(self, filename, directory, extension):
        # Set the variables for the function.
        opened = False
    
        # Loop until it is safe to write to the file
        while not opened:
            # Check if the file exists
            if os.path.isfile(filename):
                # The file exists so ask the user if they want to overwrite it
                replace = input("ERROR: File " + filename + "exists.  Would you like to replace it? (y/n)")
                # Check user input
                if not "n" in replace:
                    # Exit the loop because we will just overwrite the file.
                    opened = True
                else:
                    # Otherwise ask the user for a new filename
                    name = input("Please enter new filename: ")
                    # Check for blank input
                    if name == "":
                        # If it is blank input set the filename as an underscore.
                        name = "_"
                    # Create the new file path by combining the directory, name, and extension.
                    filename = directory + name + extension
            else:
                # Otherwise the file does not exist so it is safe to write to.
                opened = True
    
        # Return the filename with full path no matter what.
        return filename

if __name__ == '__main__':
    # Execute the installer with CLI set to true.
    Setup(True)
    


