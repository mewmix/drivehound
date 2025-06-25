import pytest
from drivehound.colors import get_color_hex


def test_get_color_hex_valid():
    assert get_color_hex("red") == "#FF0000"


def test_get_color_hex_invalid():
    with pytest.raises(ValueError):
        get_color_hex("notacolor")
