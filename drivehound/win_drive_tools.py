# drivehound/win_drive_tools.py

import os
import binascii
import subprocess
from pathlib import Path
import re
import logging

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
    """Opens a Windows drive partition in raw mode."""
    letter = letter.rstrip(":")  # Ensure only one colon
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

class DriveChunkReader:
    """
    A minimal context manager that wraps a file-like object
    and provides a .read_chunk() method for chunked reading.
    """
    def __init__(self, file_obj, sector_size=512, chunk_size=512*1024):
        self.file_obj = file_obj
        self.sector_size = sector_size  # Not strictly used here, but kept for clarity
        self.chunk_size = chunk_size
        self.position = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def read_chunk(self):
        data = self.file_obj.read(self.chunk_size)
        if data:
            self.position += len(data)
        return data

    def close(self):
        self.file_obj.close()

def open_drive(drive, mode="rb", sector_size=None, chunk_size=None):
    """
    Opens a Windows or POSIX drive, detecting whether the input is a physical drive or a file.

    Args:
        drive (str): The drive identifier (e.g., 'C:', '\\.\PhysicalDrive0', '/dev/sda1')
        mode (str): Mode to open the drive/file (default 'rb')
        sector_size (int, optional): Sector size for chunk reading
        chunk_size (int, optional): Chunk size for reading

    Returns:
        File object or DriveChunkReader: Depending on the parameters
    """
    # Regular expression to match drive letters like 'E:'
    drive_letter_pattern = re.compile(r'^[A-Za-z]:$')

    logging.debug(f"Attempting to open drive: {drive} with mode: {mode}")

    if drive_letter_pattern.match(drive):
        # It's a drive letter, open as partition
        logging.debug(f"Detected drive letter: {drive}")
        f = open_windows_partition(drive, mode=mode)
    elif os.path.isfile(drive):
        # It's a regular file
        logging.debug(f"Detected regular file: {drive}")
        f = open(drive, mode)
    elif os.name == "nt":
        # It's a physical drive or other special device
        logging.debug(f"Detected special device on Windows: {drive}")
        f = open_windows_partition(drive, mode=mode)
    else:
        # Assume a raw device path in Linux/macOS
        logging.debug(f"Detected POSIX raw device path: {drive}")
        f = open(drive, mode)

    if sector_size is not None and chunk_size is not None:
        return DriveChunkReader(f, sector_size, chunk_size)
    
    return f

def list_partitions():
    """
    Lists available partitions on the system.

    Returns:
        list: A list of partition identifiers (device paths for POSIX, drive letters for Windows).
    """
    partitions = []
    try:
        if os.name == 'posix':
            cmd = "df -hP"  # Ensure POSIX format for reliable parsing
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode().splitlines()
            for line in output:
                if not line.strip() or line.startswith("Filesystem"):
                    continue  # Skip header or empty lines
                parts = line.split()
                if parts:
                    partitions.append(parts[0])  # Only add the device path (e.g., "/dev/sda3")

        elif os.name == 'nt':
            cmd = "wmic logicaldisk get name"
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode().splitlines()
            for line in output:
                line = line.strip()
                if line and not line.startswith("Name"):
                    partitions.append(line)  # Only add the drive letter (e.g., "C:")

    except subprocess.CalledProcessError:
        logging.error("Error: Unable to list partitions.")
    
    return partitions

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
