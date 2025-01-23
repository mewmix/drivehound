import pytest
from drivehound.color_utils import hex_to_rgb, colored_text

def test_hex_to_rgb():
    assert hex_to_rgb("#FFAABB") == (255, 170, 187)

def test_colored_text():
    assert "\033[" in colored_text("Test", "red")  # Contains ANSI escape code
