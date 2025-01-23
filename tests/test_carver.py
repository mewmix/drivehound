import pytest
import os
from drivehound.carver import Carver

SIGNATURES = {
    "test": (b"\x00\x01\x02", None, ".bin")
}

@pytest.fixture
def carver():
    return Carver("test", SIGNATURES, output_dir="test_output")

def test_carver_init(carver):
    assert carver.signature_key == "test"
    assert os.path.exists(carver.output_dir)
