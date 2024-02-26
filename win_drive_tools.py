import binascii
import os

#binascii is only used to convery binary to hex consistently with different types. The rest of our functions are pure python.


# Opening a physical windows drive
def open_physical_drive(
    number,
    mode="rb",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
):
    """
    Opens a physical drive in read binary mode by default
    The numbering starts with 0
    """
    return open(
        fr"\\.\PhysicalDrive{number}",
        mode,
        buffering,
        encoding,
        errors,
        newline,
        closefd,
        opener,
    )

#Opening a windows partition
def open_windows_partition(
    letter,
    mode="rb",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
):
    """
    Opens a partition of a windows drive letter in read binary mode by default
    """
    return open(
        fr"\\.\{letter}:", mode, buffering, encoding, errors, newline, closefd, opener
    )

def open_drive(drive, mode='rb'):
    """
    Opens a drive based on the identifier provided. Can open both physical drives and partitions in various modes.

    Parameters:
    - drive: An integer representing a physical drive number, or a string representing a partition letter.
    - mode: The mode in which to open the file. Default is 'rb' (read binary), but can be changed to 'wb', 'ab', etc.

    Returns:
    - A file object corresponding to the opened drive or partition.
    """
    if isinstance(drive, str):
        # Pass the mode argument to open a windows partition
        return open_windows_partition(drive, mode=mode)
    elif isinstance(drive, int):
        # Pass the mode argument to open a physical drive
        return open_physical_drive(drive, mode=mode)
    else:
        raise ValueError("Drive must be a string (partition letter) or an integer (physical drive number)")

# Defines a function to read sectors from a physical drive.
def read_and_print_sectors(drive, num_sectors):
    """Defines a function to read sectors from a physical drive.

    Args:
        drive_number (_int_): the _physical_ drive number
        num_sectors (_int_): _number of sectors to read_

    Returns:
        _sectors_: _a list of sector data in bytes_
    """
     # If drive is a letter (partition)
    drive = open_drive(drive)
    sector_size = 512
    sectors = []
        
    for i in range(num_sectors):
        sector_data = drive.read(sector_size)
        sectors.append(sector_data)
        
    return binary_to_hex(sector_data)            
            # Print the sector header
      #  print(f"============ Sector {i} ============")
            
            # Print the sector data in hex format
       # print(binary_to_hex(sector_data))



# # Defines a function to read sectors from a physical drive.
# def read_and_save_sectors(drive, num_sectors):
#     """Defines a function to read sectors from a physical drive.

#     Args:
#         drive_number (_int_): the _physical_ drive number
#         num_sectors (_int_): _number of sectors to read_

#     Returns:
#         _sectors_: _a list of sector data in bytes_
#     """
#      # If drive is a letter (partition)
#     if isinstance(drive, str):
#             drive = open_windows_partition(drive)
#         # If drive is a number (physical drive)
#     else:
#         if isinstance(drive, int):     
#             drive = open_physical_drive(drive)
#     sector_size = 512
#     sectors = []
        
#     for i in range(num_sectors):
#         sector_data = drive.read(sector_size)
#         sectors.append(sector_data)
#         output_file=(f"sample_with_{num_sectors}_sector.bin")    
#             # Print the sector header
#         #print(f"============ Sector {i} ============")
#         with open(output_file, 'wb') as output:    
#             # Print the sector data in hex format
#             #converted = binary_to_hex(sector_data)            

#             #output.write(converted.encode('utf-8'))
#             output.write(sector_data)


# Function to convert binary data to hex and display
def binary_to_hex(binary_data):
    """_summary_

    Args:
        binary_data (_type_): _description_

    Returns:
        _type_: _description_
    """
    return binascii.hexlify(binary_data).decode('utf-8')


def read_binary_file_as_hex(file_path):
    """
    Reads a binary file and returns its content as a hexadecimal string.

    Args:
        file_path (str): Path to the binary file.

    Returns:
        str: Hexadecimal representation of the file content.
    """
    try:
        with open(file_path, 'rb') as file:
            binary_data = file.read()
            hex_data = binascii.hexlify(binary_data).decode('utf-8')
            print(hex_data)
            return hex_data
        
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def bytes_to_hex_to_integers(byte_list):
    hex_list = [byte.hex() for byte in byte_list]
    integers_list = [int(hex_str, 16) for hex_str in hex_list]
    return integers_list

def print_bytes_as_hex(byte_list):
    for byte in byte_list:
        print(byte.hex())

def read_and_save_sectors(drive, num_sectors, output_file):
    """
    Reads and saves sectors from a physical drive to a binary file.

    Args:
        drive: Opened file object of the drive.
        num_sectors (int): Number of sectors to read.
        output_file (str): Path to the output file to write sectors.
    """
    sector_size = 512
    with open(output_file, 'wb') as output:
        for _ in range(num_sectors):
            sector_data = drive.read(sector_size)
            if sector_data:
                output.write(sector_data)

def snapshot_drive(drive, sectors, output_file):
    """
    Creates a snapshot of the drive by reading specified sectors and saving them to a file.

    Args:
        drive (int or str): Physical drive number or partition letter.
        sectors (int): Number of sectors to snapshot.
        output_file (str): Path to the output file to save the snapshot.
    """
    # Open the drive based on the input type (partition letter or physical drive number)
    drive_obj = open_drive(drive)
    try:
        read_and_save_sectors(drive_obj, sectors, output_file)
        print(f"Completed writing {sectors} sectors to {output_file}")
    finally:
        drive_obj.close()


def write_test_to_drive(drive_letter, data, test_file_name="testfile.txt"):
    """
    Writes a small test file to the specified drive.

    Parameters:
    - drive_letter (str): Letter of the drive where the test file will be written.
    - data (str): Data to be written to the test file.
    - test_file_name (str): Name of the test file to be created.

    This function will attempt to create a new file at the root of the specified drive
    and write the provided data into it. This is a safer alternative to writing directly
    to the drive's sectors and does not require administrative privileges.
    """
    file_path = f"{drive_letter}:\\{test_file_name}"
    try:
        with open(file_path, 'w') as test_file:
            test_file.write(data)
        print(f"Successfully wrote to {file_path}")
    except PermissionError:
        print(f"Permission denied. Could not write to {file_path}. Ensure you have the necessary permissions.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def write_to_sector(drive_number, sector_number, data, sector_size=512):
    """
    Writes data to a specific sector of a physical drive. Requires administrative privileges.

    Parameters:
    - drive_number (int): Number of the physical drive (e.g., 0 for PhysicalDrive0).
    - sector_number (int): The sector number to write to (starting from 0).
    - data (bytes): Data to be written. Should match the sector size or be padded accordingly.
    - sector_size (int): Size of the sector in bytes. Defaults to 512.
    
    Note: This function is dangerous and can cause data loss or corruption.
    """
    drive_path = f"\\\\.\\PhysicalDrive{drive_number}"
    if not isinstance(data, bytes):
        raise ValueError("Data must be of type bytes.")
    # Pad the data if its length is less than the sector size
    if len(data) < sector_size:
        data = data.ljust(sector_size, b'\x00')  # Pad with null bytes
    
    try:
        with open(drive_path, 'r+b') as drive:
            # Seek to the start of the target sector
            drive.seek((sector_number * sector_size) + os.SEEK_SET)
            # Write the data to the sector
            drive.write(data)
        print(f"Successfully wrote to sector {sector_number} of {drive_path}")
    except PermissionError:
        print("Permission denied. Could not write to the drive. Ensure you have administrative privileges.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def ascii_hex_converter(input_string):
    # Function to check if a string represents a valid hexadecimal number
    def is_hex(s):
        try:
            int(s, 16)
            return True
        except ValueError:
            return False

    # Convert ASCII to Hex
    def ascii_to_hex(ascii_str):
        return ''.join(format(ord(char), '02x') for char in ascii_str)

    # Convert Hex to ASCII
    def hex_to_ascii(hex_str):
        hex_str = hex_str.replace(" ", "")  # Removing spaces if any
        return ''.join(chr(int(hex_str[i:i+2], 16)) for i in range(0, len(hex_str), 2))

    # Detect and convert
    if all(c in '0123456789abcdefABCDEF' for c in input_string) and is_hex(input_string):
        return hex_to_ascii(input_string)
    else:
        return ascii_to_hex(input_string)