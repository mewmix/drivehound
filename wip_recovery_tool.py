import os
import subprocess
from collections import defaultdict
from win_drive_tools import open_physical_drive, open_windows_partition

# Function to list disk partitions
def list_partitions():
    """Easy crossplatform handler to list partitions.
    """
    if os.name == 'posix': # Linux and Mac
        cmd = "df -h"
    elif os.name == 'nt': # Windows
        cmd = "fsutil fsinfo drives"
    else:
        print("Operating system not supported.")
        return

    partitions = subprocess.check_output(cmd, shell=True).decode()
    print(partitions)

# Function to recover data
def recover_data(drive):
    """Cross platform Magic Signature retrieval.
 For Linux and MacOS: use the full path to the drive (eg: /dev/sda1)
 For Windows: use the drive letter (eg: 'C') for partitions or drive number for physical drive,

    Args:
        drive (_type_): _Accepts int or string input_
        signatures (_type_): _The File Signatures Dictionary to Use_
    """
    # For Linux and Mac
    if os.name == 'posix':
        drive = open(drive, "rb")
    # For Windows
    elif os.name == 'nt':
        # If drive is a letter (partition)
        if isinstance(drive, str):
            drive = open_windows_partition(drive)
        # If drive is a number (physical drive)
        else:
            if isinstance(drive, int):     
                drive = open_physical_drive(drive)

    size = 512  # Size of bytes to read
    byte = drive.read(size)
    offs = 0
    # Recovered file ID
    files = defaultdict(int)
    sector = 0

    while byte:
        print(f"Reading sector: {sector}")
        
        for file_type, sigs in signatures.items():
            start_sig, end_sig, ext = sigs
            found = byte.find(start_sig)

            if found >= 0:
                drec = True
                print(f'==== Found {file_type} at location: {str(hex(found + (size * offs)))} ====')
                filename = f'{file_type}_{files[file_type]}{ext}'

                with open(filename, "wb") as fileN:
                    print(f"Writing found {file_type} to file: {filename}")
                    fileN.write(byte[found:])
                    while drec:
                        byte = drive.read(size)
                        bfind = byte.find(end_sig)

                        if bfind >= 0:
                            fileN.write(byte[:bfind + len(end_sig)])  # Write the entire end signature
                            drive.seek((offs + 1) * size)
                            print(f'==== Wrote {file_type} to location: {filename} ====\n')
                            files[file_type] += 1
                            drec = False
                        else:
                            fileN.write(byte)  # Write the whole buffer if the end signature is not found

        offs += 1
        sector += 1
        byte = drive.read(size)


    print(f"Finished reading sectors! The last sector read was: {sector}")
    drive.close()


# File signatures dictionary. Add more signatures as needed.
signatures = {
    "jpg": (bytes.fromhex("FFD8FFE000104A46"), bytes.fromhex("FFD9"), ".jpg"),
    "gif": (bytes.fromhex("474946383761"), bytes.fromhex("003B"), ".gif"),
    "png": (bytes.fromhex("89504E470D0A1A0A"), bytes.fromhex("49454E44AE426082"), ".png"),
    "rtf": (bytes.fromhex("7B5C727466"), bytes.fromhex("7D"), ".rtf"),
    "mpg": (bytes.fromhex("000001BA"), bytes.fromhex("000001B9"), ".mpg"),
}




