import binascii


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
    if isinstance(drive, str):
            drive = open_windows_partition(drive)
        # If drive is a number (physical drive)
    else:
        if isinstance(drive, int):     
            drive = open_physical_drive(drive)
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



# Defines a function to read sectors from a physical drive.
def read_and_save_sectors(drive, num_sectors):
    """Defines a function to read sectors from a physical drive.

    Args:
        drive_number (_int_): the _physical_ drive number
        num_sectors (_int_): _number of sectors to read_

    Returns:
        _sectors_: _a list of sector data in bytes_
    """
     # If drive is a letter (partition)
    if isinstance(drive, str):
            drive = open_windows_partition(drive)
        # If drive is a number (physical drive)
    else:
        if isinstance(drive, int):     
            drive = open_physical_drive(drive)
    sector_size = 512
    sectors = []
        
    for i in range(num_sectors):
        sector_data = drive.read(sector_size)
        sectors.append(sector_data)
        output_file=(f"sample_with_{num_sectors}_sector.bin")    
            # Print the sector header
        #print(f"============ Sector {i} ============")
        with open(output_file, 'wb') as output:    
            # Print the sector data in hex format
            #converted = binary_to_hex(sector_data)            

            #output.write(converted.encode('utf-8'))
            output.write(sector_data)


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

def snapshot_drive(sectors):
    for i in range(sectors):
        read_and_save_sectors(drive=1, num_sectors=i)
        print(f"Writing sector {i}")