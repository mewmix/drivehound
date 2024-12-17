# enhanced_recovery_tool.py

import os
import logging
import time
from collections import defaultdict
from file_signatures import FILE_SIGNATURES
from win_drive_tools import open_drive

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class DriveReader:
    def __init__(self, drive, sector_size=512, chunk_size=512*1024):
        """
        A reader class that abstracts reading from a drive or partition.
        
        Args:
            drive: The drive identifier (e.g., 'C' for Windows partition, or '/dev/sda1' on Linux)
            sector_size: The sector size in bytes (default: 512)
            chunk_size: The size of data to read per iteration in bytes for performance. 
                        A larger chunk_size can significantly improve performance when scanning large drives.
        """
        self.drive_path = drive
        self.sector_size = sector_size
        self.chunk_size = chunk_size
        self.handle = None
        self.position = 0

    def __enter__(self):
        self.handle = open_drive(self.drive_path, 'rb')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.handle:
            self.handle.close()

    def seek(self, offset):
        self.handle.seek(offset, os.SEEK_SET)
        self.position = offset

    def read_chunk(self):
        """
        Reads a chunk of data from the drive. Returns an empty bytes object if EOF is reached.
        """
        data = self.handle.read(self.chunk_size)
        self.position += len(data)
        return data


class RecoveryTool:
    def __init__(self, signatures=FILE_SIGNATURES, 
                 sector_size=512, 
                 chunk_size=512*1024, 
                 output_dir="recovered_files", 
                 target_filetype=None,
                 verbose=True):
        """
        RecoveryTool provides a more verbose, tuned, and potentially faster file recovery approach.

        Args:
            signatures (dict): Dictionary of file signatures: { "type": (start_sig, end_sig, extension) }
            sector_size (int): Sector size for offset calculations.
            chunk_size (int): How many bytes to read per iteration; larger is generally faster.
            output_dir (str): Directory to store recovered files.
            target_filetype (str): If provided, only recover this specific file type.
            verbose (bool): If True, print verbose logs.
        """
        self.signatures = signatures
        self.sector_size = sector_size
        self.chunk_size = chunk_size
        self.output_dir = output_dir
        self.target_filetype = target_filetype
        self.verbose = verbose
        os.makedirs(self.output_dir, exist_ok=True)

        # Filter signatures if a target_filetype is specified
        if self.target_filetype:
            if self.target_filetype not in self.signatures:
                raise ValueError(f"Target filetype '{self.target_filetype}' not in signatures.")
            # Restrict to just that one
            self.signatures = {self.target_filetype: self.signatures[self.target_filetype]}
        
        # Filter out any signatures that don't have a valid start signature
        # We only handle start-signature based carving here. 
        # If a format doesn't have a start signature, it is very tricky to carve reliably.
        valid_signatures = {k: v for k, v in self.signatures.items() if v[0] is not None}
        if not valid_signatures:
            logging.warning("No signatures with a valid start signature found. Nothing will be carved.")
        self.signatures = valid_signatures

        if self.signatures:
            self.max_start_sig_len = max(len(s[0]) for s in self.signatures.values())
        else:
            # No valid signatures, just set a default
            self.max_start_sig_len = 1

    def recover_data(self, drive):
        """
        Recovers data from a specified drive using known file signatures.
        
        Args:
            drive: The drive identifier (e.g., 'C' for Windows partition, or '/dev/sda1' on Linux)
        """
        start_time = time.time()
        files_found = defaultdict(int)

        # If no signatures with start bytes, just return immediately
        if not self.signatures:
            if self.verbose:
                logging.info("No valid start-signature-based files to recover.")
            return files_found

        buffer = b""
        total_files_carved = 0
        active_extractions = []  # Each element: { 'file_type', 'outfile', 'end_sig', 'start_offset' }

        with DriveReader(drive, self.sector_size, self.chunk_size) as reader:
            while True:
                chunk = reader.read_chunk()
                if not chunk:
                    # EOF reached
                    break

                buffer += chunk

                # Handle continuing extraction for files that are currently being carved.
                new_active = []
                for extraction in active_extractions:
                    if extraction['end_sig']:
                        end_pos = buffer.find(extraction['end_sig'])
                        if end_pos >= 0:
                            # Found the end of the file
                            extraction['outfile'].write(buffer[:end_pos + len(extraction['end_sig'])])
                            extraction['outfile'].close()
                            if self.verbose:
                                logging.info(f"Completed {extraction['file_type']} file started at offset {hex(extraction['start_offset'])}")
                            buffer = buffer[end_pos + len(extraction['end_sig']):]
                            continue
                        else:
                            # No end found yet, write entire buffer and continue
                            extraction['outfile'].write(buffer)
                            buffer = b""
                            new_active.append(extraction)
                    else:
                        # No end signature, write until EOF
                        extraction['outfile'].write(buffer)
                        buffer = b""
                        new_active.append(extraction)

                active_extractions = new_active

                # Try to find new start signatures if buffer has data
                # and we haven't consumed everything with ongoing extractions.
                if buffer:
                    something_found = True
                    while something_found and self.signatures:
                        something_found = False
                        for file_type, (start_sig, end_sig, ext) in self.signatures.items():
                            start_idx = buffer.find(start_sig)
                            if start_idx >= 0:
                                start_offset = (reader.position - len(buffer)) + start_idx
                                filename = f"{file_type}_{files_found[file_type]}{ext}"
                                files_found[file_type] += 1
                                total_files_carved += 1
                                if self.verbose:
                                    logging.info(f"Found {file_type} at offset {hex(start_offset)}, saving as {filename}")
                                out_path = os.path.join(self.output_dir, filename)
                                outfile = open(out_path, "wb")
                                # Write from start_idx onwards
                                outfile.write(buffer[start_idx:])
                                # Clear the buffer because we've written everything after start_idx
                                buffer = b""
                                # Track extraction
                                active_extractions.append({
                                    'file_type': file_type,
                                    'outfile': outfile,
                                    'end_sig': end_sig,
                                    'start_offset': start_offset
                                })
                                something_found = True
                                # Break to re-check from start since buffer changed
                                break

                    # Keep some buffer tail if no active extractions:
                    if not active_extractions and self.max_start_sig_len > 1:
                        max_retain = self.max_start_sig_len - 1
                        buffer = buffer[-max_retain:]

            # End of file: Close any extractions without end sig
            for extraction in active_extractions:
                extraction['outfile'].write(buffer)
                extraction['outfile'].close()
                if self.verbose:
                    logging.info(f"Completed {extraction['file_type']} file (no end signature) started at offset {hex(extraction['start_offset'])}")

        end_time = time.time()
        elapsed = end_time - start_time
        if self.verbose:
            logging.info(f"Recovery complete. Total files carved: {total_files_carved}. Time taken: {elapsed:.2f} seconds.")
            for ftype, count in files_found.items():
                logging.info(f"  {ftype}: {count} files recovered")

        return files_found
