# carver.py
import os
import logging

# Example usage: Carve a specific file type from a disk image or raw file data.
# This module provides a Carver class that can:
# - Tune into a specific file format signature (start and optional end marker)
# - Search through large raw data (like a disk image or memory dump)
# - Extract all occurrences of files matching that signature
#
# It supports partial searching, offset-based adjustments, and chunked reading for large files.

class Carver:
    def __init__(self, signature_key, signatures_dict, sector_size=512, output_dir="carved_output"):
        """
        Initialize the Carver with a specific signature key and a dictionary of signatures.

        Args:
            signature_key (str): The key from the signatures_dict to carve.
            signatures_dict (dict): Dictionary of signatures in format:
                signature_key: (start_bytes, end_bytes_or_None, extension)
            sector_size (int): Sector size to read at a time. Defaults to 512 for disk-like sources.
            output_dir (str): Directory to store carved files.
        """
        self.signature_key = signature_key
        self.signatures = signatures_dict
        if signature_key not in self.signatures:
            raise ValueError(f"Signature key {signature_key} not found in provided dictionary.")
        self.start_sig, self.end_sig, self.extension = self.signatures[signature_key]
        self.sector_size = sector_size
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self._file_counter = 0

    def carve_from_file(self, source_path):
        """
        Carve files of the specified signature type from the given source file.

        Args:
            source_path (str): Path to the source file (e.g., disk image, memory dump)

        Returns:
            int: The number of files carved.
        """
        # Open in binary mode
        with open(source_path, "rb") as src:
            return self.carve_from_stream(src)

    def carve_from_stream(self, src):
        """
        Carve files of the specified signature type from a binary stream.

        Args:
            src (file-like): A binary stream with a read() method.

        Returns:
            int: The number of files carved.
        """
        logging.info(f"Starting carving for {self.signature_key} with extension {self.extension}")

        # We will read in chunks and search for the start pattern.
        # Once found, we will keep reading until the end pattern is located (if end pattern is defined).
        total_carved = 0
        buffer = b""
        chunk_size = self.sector_size * 64  # read bigger chunks for better performance
        eof_reached = False
        file_in_progress = False
        outfile = None

        while not eof_reached:
            data = src.read(chunk_size)
            if not data:
                eof_reached = True
            else:
                buffer += data

            # Process the buffer
            # If we are not currently extracting a file, look for start_sig
            if not file_in_progress:
                start_pos = buffer.find(self.start_sig)
                if start_pos >= 0:
                    # Found a start signature
                    file_in_progress = True
                    # Create a new output file
                    out_name = f"{self.signature_key}_{self._file_counter}{self.extension}"
                    out_path = os.path.join(self.output_dir, out_name)
                    outfile = open(out_path, "wb")
                    # Write from start_pos onwards
                    outfile.write(buffer[start_pos:])
                    # Trim buffer to only what was beyond start_pos
                    buffer = b""
                    self._file_counter += 1
                    total_carved += 1
                else:
                    # Keep buffer small if we didn't find anything: avoid memory blowup
                    # Retain last len(start_sig)-1 bytes to not miss a signature crossing chunks
                    max_retain = len(self.start_sig) - 1 if len(self.start_sig) > 1 else 1
                    buffer = buffer[-max_retain:]
            else:
                # We are currently writing to a file. If end_sig is None, we write until EOF.
                # If end_sig is defined, search for it
                if self.end_sig is not None:
                    end_pos = buffer.find(self.end_sig)
                    if end_pos >= 0:
                        # End found, write up to end signature
                        outfile.write(buffer[:end_pos + len(self.end_sig)])
                        outfile.close()
                        outfile = None
                        file_in_progress = False
                        # Discard everything up to end_pos
                        buffer = buffer[end_pos + len(self.end_sig):]
                        # After finishing one file, we might want to immediately look if another file start is here
                        # We'll just continue the loop to handle that in next iteration
                    else:
                        # No end signature found, write entire buffer and reset it
                        outfile.write(buffer)
                        buffer = b""
                else:
                    # No end signature, we keep writing until EOF
                    if eof_reached:
                        # Write whatever left in buffer
                        outfile.write(buffer)
                        buffer = b""
                        outfile.close()
                        outfile = None
                        file_in_progress = False
                    else:
                        # Just keep writing
                        outfile.write(buffer)
                        buffer = b""

        # If file_in_progress still True at the end (no end found and not ended):
        if file_in_progress and outfile:
            outfile.write(buffer)
            outfile.close()
            file_in_progress = False

        logging.info(f"Carving complete. Total files carved: {total_carved}")
        return total_carved
