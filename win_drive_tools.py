
# win_drive_tools.py

import os
import binascii
import subprocess
from pathlib import Path

def open_physical_drive(
    number,
    mode="rb",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None
):
    return open(
        fr"\\.\PhysicalDrive{number}",
        mode,
        buffering,
        encoding,
        errors,
        newline,
        closefd,
        opener
    )

def open_windows_partition(
    letter,
    mode="rb",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None
):
    return open(
        fr"\\.\{letter}:",
        mode,
        buffering,
        encoding,
        errors,
        newline,
        closefd,
        opener
    )

def open_drive(drive, mode='rb'):
    # Cross-platform logic for opening a drive/partition.
    # For POSIX: drive should be a path like "/dev/sda", "/dev/sda1", etc.
    # For Windows: drive can be a letter like 'C', or an integer for a physical drive.
    if os.name == 'posix':
        if isinstance(drive, str):
            return open(drive, mode)
        else:
            raise ValueError("On POSIX systems, the drive must be a string representing a device path.")
    elif os.name == 'nt':
        if isinstance(drive, str):
            return open_windows_partition(drive, mode=mode)
        elif isinstance(drive, int):
            return open_physical_drive(drive, mode=mode)
        else:
            raise ValueError("On Windows, the drive must be a string (partition letter) or an integer (physical drive).")
    else:
        raise OSError("Unsupported operating system.")

def list_partitions():
    # Cross-platform listing of partitions.
    # This is simplistic and may need refinement per platform.
    if os.name == 'posix':
        cmd = "df -h"
    elif os.name == 'nt':
        cmd = "wmic logicaldisk get name"
    else:
        return []
    output = subprocess.check_output(cmd, shell=True).decode().strip().split('\n')
    return [line.strip() for line in output if line.strip()]

def binary_to_hex(binary_data):
    return binascii.hexlify(binary_data).decode('utf-8')

def ascii_hex_converter(input_string):
    def is_hex(s):
        try:
            int(s, 16)
            return True
        except ValueError:
            return False
    def ascii_to_hex(ascii_str):
        return ''.join(format(ord(char), '02x') for char in ascii_str)
    def hex_to_ascii(hex_str):
        hex_str = hex_str.replace(" ", "")
        return ''.join(chr(int(hex_str[i:i+2], 16)) for i in range(0, len(hex_str), 2))

    input_stripped = input_string.strip()
    if all(c in '0123456789abcdefABCDEF' for c in input_stripped) and is_hex(input_stripped):
        return hex_to_ascii(input_stripped)
    else:
        return ascii_to_hex(input_stripped)
