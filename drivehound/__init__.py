# drivehound/__init__.py

from .hound import Hound
from .carver import Carver
from .win_drive_tools import open_drive, list_partitions
from .color_utils import (
    colored_text,
    colored_bg_text,
    print_colored,
    print_colored_bg
)
from .file_signatures import FILE_SIGNATURES
from .colors import get_color_hex, COLOR_PALETTE
from .ascii_utils import scale_ascii_art
from .logo import LOGO

__all__ = [
    'Hound',
    'Carver',
    'open_drive',
    'list_partitions',
    'scale_ascii_art',
]
