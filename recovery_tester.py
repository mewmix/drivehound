# recovery_tester.py

from wip_recovery_tool import RecoveryTool
from win_drive_tools import list_partitions

# Example usage: scanning a specific drive
# Change the drive value to suit your platform. On Linux, something like "/dev/sda".
# On Windows, a partition letter like "D" or a physical drive number like 0.
# Note: Make sure you have the necessary permissions.

if __name__ == "__main__":
    print("Available partitions:")
    for p in list_partitions():
        print(p)

    # Example usage:
    # On Windows, to scan D drive: drive = "D"
    # On Linux, to scan /dev/sda1: drive = "/dev/sda1"
    # On Mac, something similar to Linux.
    
    # Adjust as needed before running.
    drive = "D"
    recovery_tool = RecoveryTool()
    recovery_tool.recover_data(drive=drive)
