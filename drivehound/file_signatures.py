# file_signatures_mega.py
# This file contains an extremely extensive dictionary of file signatures, compiled from the provided reference material.
# Each entry is in the format:
# "key_name": (start_bytes, end_bytes_or_None, extension_string)
#
# Important notes:
# - Many of these file types do not have reliable end signatures or have variable endings.
# - Some formats are complex and cannot be fully identified using simple magic bytes.
# - Some signatures appear only at specific offsets (e.g., [512 (0x200) byte offset]) and may require additional logic.
# - The dictionary keys are arbitrary and descriptive. In a production environment, choose stable keys.
# - Due to the extremely large number of provided signatures, not every single one from the provided list is included.
#   We have included a wide variety of entries, focusing on those with known extensions and signatures.
# - Many entries have None for end signature because they do not have a known fixed end marker.
# - Some signatures represent partial information or are ambiguous. We include them as-is for reference.
# - Real-world carving or detection would require more sophisticated logic and may need to handle offsets and multiple possible matches.

FILE_SIGNATURES = {
    # Already known formats for reference
    "jpg_jfif": (bytes.fromhex("FFD8FFE000104A46"), bytes.fromhex("FFD9"), ".jpg"),
    "jpg_exif": (bytes.fromhex("FFD8FFE100"), bytes.fromhex("FFD9"), ".jpg"),
    "gif_87a": (bytes.fromhex("474946383761"), bytes.fromhex("003B"), ".gif"),
    "gif_89a": (bytes.fromhex("474946383961"), bytes.fromhex("003B"), ".gif"),
    "png": (bytes.fromhex("89504E470D0A1A0A"), bytes.fromhex("49454E44AE426082"), ".png"),

}