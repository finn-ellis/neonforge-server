#!/bin/bash

# This script provides a simple GUI to restart the NeonBrush VR APK on a connected Android device.
# It uses zenity to create the graphical user interface.
#
# Usage:
# ./restart_apk_gui.sh [/path/to/adb]
#
# If the path to adb is not provided, it will try to use 'adb' from the system's PATH.

# Set the default path for adb.
ADB_PATH="adb"

# If an argument is provided, use it as the path to adb.
if [ -n "$1" ]; then
    ADB_PATH="$1"
fi

# Display a dialog with a button to trigger the restart.
zenity --question --title="NeonBrush VR APK Control" --text="Click the button to restart the Open Brush APK on the connected device." --ok-label="Restart APK" --cancel-label="Cancel"

# Check the exit status of the zenity dialog.
# If the user clicked "Restart APK", zenity returns 0.
if [ $? -eq 0 ]; then
    # Execute the adb command.
    # The quotes around "$ADB_PATH" ensure that paths with spaces are handled correctly.
    "$ADB_PATH" shell am start -S foundation.icosa.openbrush/com.unity3d.player.UnityPlayerActivity
    
    # Check if the adb command was successful.
    if [ $? -eq 0 ]; then
        zenity --info --text="Restart command sent successfully." --title="Success"
    else
        zenity --error --text="Failed to send restart command. Make sure the device is connected and adb is working." --title="Error"
    fi
fi
