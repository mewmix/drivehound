import pytest
from drivehound.hound import Hound

def test_hound_init():
    h = Hound()
    assert isinstance(h.signatures, dict)
