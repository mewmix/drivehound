# drivehound/colors.py

"""
colors.py

A comprehensive collection of named colors with their corresponding hex codes.
This module allows for easy access to a large set of colors for use in DriveHound's terminal outputs.
"""

# Dictionary of color names mapped to their hex codes
COLOR_PALETTE = {
    "black": "#000000",
    "white": "#FFFFFF",
    "red": "#FF0000",
    "green": "#00FF00",
    "blue": "#0000FF",
    "yellow": "#FFFF00",
    "cyan": "#00FFFF",
    "magenta": "#FF00FF",
    "orange": "#FFA500",
    "purple": "#800080",
    "pink": "#FFC0CB",
    "brown": "#A52A2A",
    "gray": "#808080",
    "lime": "#00FF00",
    "maroon": "#800000",
    "navy": "#000080",
    "olive": "#808000",
    "teal": "#008080",
    "silver": "#C0C0C0",
    "gold": "#FFD700",
    "coral": "#FF7F50",
    "crimson": "#DC143C",
    "indigo": "#4B0082",
    "khaki": "#F0E68C",
    "lavender": "#E6E6FA",
    "mint": "#98FF98",
    "mustard": "#FFDB58",
    "plum": "#DDA0DD",
    "salmon": "#FA8072",
    "scarlet": "#FF2400",
    "sienna": "#A0522D",
    "tan": "#D2B48C",
    "violet": "#EE82EE",
    "azure": "#F0FFFF",
    "beige": "#F5F5DC",
    "bisque": "#FFE4C4",
    "blanchedalmond": "#FFEBCD",
    "blueviolet": "#8A2BE2",
    "chartreuse": "#7FFF00",
    "darkcyan": "#008B8B",
    "darkgoldenrod": "#B8860B",
    "darkgrey": "#A9A9A9",
    "darkkhaki": "#BDB76B",
    "darkmagenta": "#8B008B",
    "darkolivegreen": "#556B2F",
    "darkorange": "#FF8C00",
    "darkorchid": "#9932CC",
    "darkred": "#8B0000",
    "darksalmon": "#E9967A",
    "darkseagreen": "#8FBC8F",
    "darkslateblue": "#483D8B",
    "darkslategray": "#2F4F4F",
    "darkturquoise": "#00CED1",
    "deeppink": "#FF1493",
    "deepskyblue": "#00BFFF",
    "dimgray": "#696969",
    "dodgerblue": "#1E90FF",
    # Add more colors as needed
}

def get_color_hex(color_name: str) -> str:
    """
    Retrieves the hex code for a given color name from the color palette.

    Args:
        color_name (str): The name of the color (case-insensitive).

    Returns:
        str: Hex code of the color.

    Raises:
        ValueError: If the color name is not found in the palette.
    """
    color_key = color_name.lower()
    if color_key in COLOR_PALETTE:
        return COLOR_PALETTE[color_key]
    else:
        raise ValueError(f"Color '{color_name}' not found in the color palette.")
