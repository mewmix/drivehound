# drivehound/color_utils.py

"""
color_utils.py

Utility functions for handling colored text output in the terminal using ANSI escape codes.
Supports both predefined color palettes and custom hex color codes.
"""

import sys
from .colors import COLOR_PALETTE, get_color_hex

def hex_to_rgb(hex_color: str):
    """
    Converts a hex color string to an RGB tuple.

    Args:
        hex_color (str): Hex color string (e.g., '#FFAABB' or 'FFAABB').

    Returns:
        tuple: (R, G, B) as integers.
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("Hex color must be in the format RRGGBB.")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (r, g, b)

def rgb_to_ansi_fg(r: int, g: int, b: int):
    """
    Creates an ANSI escape code for the foreground color.

    Args:
        r (int): Red component (0-255).
        g (int): Green component (0-255).
        b (int): Blue component (0-255).

    Returns:
        str: ANSI escape code string.
    """
    return f'\033[38;2;{r};{g};{b}m'

def rgb_to_ansi_bg(r: int, g: int, b: int):
    """
    Creates an ANSI escape code for the background color.

    Args:
        r (int): Red component (0-255).
        g (int): Green component (0-255).
        b (int): Blue component (0-255).

    Returns:
        str: ANSI escape code string.
    """
    return f'\033[48;2;{r};{g};{b}m'

def reset_ansi():
    """
    Returns the ANSI escape code to reset colors.

    Returns:
        str: ANSI reset code.
    """
    return '\033[0m'

def colored_text(text: str, color: str):
    """
    Wraps the given text with ANSI codes to display it in the specified color.
    Supports both predefined color names and custom hex color codes.

    Args:
        text (str): The text to color.
        color (str): Color name (e.g., 'red') or hex color string (e.g., '#FFAABB').

    Returns:
        str: Colored text with ANSI codes.
    """
    try:
        # Attempt to get hex code from color name
        hex_color = get_color_hex(color)
    except ValueError:
        # Assume the color is a hex code
        hex_color = color
    r, g, b = hex_to_rgb(hex_color)
    return f"{rgb_to_ansi_fg(r, g, b)}{text}{reset_ansi()}"

def colored_bg_text(text: str, color: str):
    """
    Wraps the given text with ANSI codes to display it with the specified background color.
    Supports both predefined color names and custom hex color codes.

    Args:
        text (str): The text to color.
        color (str): Color name (e.g., 'blue') or hex color string (e.g., '#0000FF').

    Returns:
        str: Text with colored background using ANSI codes.
    """
    try:
        # Attempt to get hex code from color name
        hex_color = get_color_hex(color)
    except ValueError:
        # Assume the color is a hex code
        hex_color = color
    r, g, b = hex_to_rgb(hex_color)
    return f"{rgb_to_ansi_bg(r, g, b)}{text}{reset_ansi()}"

def print_colored(text: str, color: str):
    """
    Prints the given text in the specified color.

    Args:
        text (str): The text to print.
        color (str): Color name or hex color string.
    """
    colored = colored_text(text, color)
    print(colored)

def print_colored_bg(text: str, color: str):
    """
    Prints the given text with the specified background color.

    Args:
        text (str): The text to print.
        color (str): Color name or hex color string.
    """
    colored = colored_bg_text(text, color)
    print(colored)
