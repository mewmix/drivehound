# drivehound/recovery_tester.py

from .hound import Hound
from .win_drive_tools import list_partitions
from .color_utils import colored_text
from .ascii_utils import scale_ascii_art
from .logo import LOGO
import sys
import time
import logging

def display_ascii_art(scale: int, color: str):
    scaled_logo = scale_ascii_art(LOGO, scale)
    colored_logo = colored_text(scaled_logo, color)
    print(colored_logo)

# ANSI color mapping for log messages
LOG_COLORS = {
    "found": "yellow",
    "completed": "green",
    "error": "red",
    "info": "cyan"
}

class ColorFormatter(logging.Formatter):
    """
    Custom logging formatter to apply colors to log messages.
    """
    def format(self, record):
        log_msg = super().format(record)

        if "Found" in record.msg:
            log_msg = colored_text(log_msg, LOG_COLORS["found"])
        elif "Completed" in record.msg:
            log_msg = colored_text(log_msg, LOG_COLORS["completed"])
        elif record.levelname == "ERROR":
            log_msg = colored_text(log_msg, LOG_COLORS["error"])
        elif record.levelname == "INFO":
            log_msg = colored_text(log_msg, LOG_COLORS["info"])

        return log_msg

def setup_logging(log_file="recovery_tester.log"):
    """
    Configures logging to allow colored output in the console.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # File handler (no colors)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

    # Console handler (with colors)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColorFormatter('%(asctime)s [%(levelname)s] %(message)s'))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def main():
    # Configuration Parameters
    scale = 2
    color = "#00FF00"  # Green
    log_file = "recovery_tester.log"
    
    # Setup Logging
    setup_logging()
    
    # Display ASCII Art
    print("\n")
    display_ascii_art(scale=scale, color=color)
    print("\n")
    
    print(colored_text("drivehound recovery tool", "white"))
    print("=========================\n")
    
    # List Available Partitions
    partitions = list_partitions()
    if not partitions:
        logging.error("No partitions found or unable to list partitions.")
        sys.exit(1)
    
    print("Available partitions:")
    print("=====================")
    for idx, partition in enumerate(partitions, start=1):
        print(f"{idx}. {partition}")
    print("=====================\n")
    
    # Prompt User to Select a Drive
    while True:
        try:
            selection = input(f"Enter the number of the drive to scan (1-{len(partitions)}): ").strip()
            if not selection.isdigit():
                raise ValueError("Input must be a number corresponding to the drive.")
            selection = int(selection)
            if 1 <= selection <= len(partitions):
                drive = partitions[selection - 1]
                break
            else:
                raise ValueError(f"Please enter a number between 1 and {len(partitions)}.")
        except ValueError as ve:
            print(f"Invalid input: {ve}\nPlease try again.\n")
    
    # Confirm Recovery Action
    while True:
        confirmation = input(f"Are you sure you want to scan drive '{drive}' for file recovery? (y/n): ").strip().lower()
        if confirmation in ['y', 'yes']:
            break
        elif confirmation in ['n', 'no']:
            print(colored_text("Recovery operation cancelled by user.", "red"))
            sys.exit(0)
        else:
            print("Please enter 'y' or 'n'.")
    
    # Initialize Hound and Start Recovery
    hound = Hound(verbose=True)
    
    # Display Progress
    print("Starting recovery...")
    start_time = time.time()
    recovered_files = hound.recover_files(drive=drive)
    end_time = time.time()
    
    # Display Recovery Results
    print("\nRecovery Complete.")
    print("===================")
    if recovered_files:
        for file_type, count in recovered_files.items():
            colored_output = colored_text(f"{file_type.upper()}: {count} file(s) recovered.", "orange")
            print(colored_output)
    else:
        print(colored_text("No files were recovered.", "red"))
    print("===================\n")
    print(colored_text(f"Recovered files are saved in the '{hound.output_dir}' directory.", "cyan"))
    print(colored_text(f"Detailed logs can be found in '{log_file}'.", "cyan"))
    print(colored_text(f"Time taken: {end_time - start_time:.2f} seconds.", "cyan"))
