import pytest
from drivehound.ascii_utils import scale_ascii_art


def test_scale_ascii_art_simple():
    art = "ab\ncd"
    expected = "aabb\naabb\nccdd\nccdd\n"
    assert scale_ascii_art(art, 2) == expected
