# ascii_art_utils.py

def scale_ascii_art(art: str, scale: int) -> str:
    """
    Scales the given ASCII art by the specified scale factor.

    Args:
        art (str): The original ASCII art as a multi-line string.
        scale (int): The scale factor (e.g., 2 doubles the size).

    Returns:
        str: The scaled ASCII art.
    """
    scaled_art = ""
    for line in art.splitlines():
        scaled_line = ""
        for char in line:
            scaled_line += char * scale
        for _ in range(scale):
            scaled_art += scaled_line + "\n"
    return scaled_art
