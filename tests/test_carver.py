import os
from io import BytesIO
import pytest
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

def test_carver_carve_from_stream(tmp_path):
    sigs = {"foo": (b"START", b"END", ".txt")}
    carver = Carver("foo", sigs, output_dir=str(tmp_path))
    data = b"junkSTARThelloEND"
    count = carver.carve_from_stream(BytesIO(data))
    assert count == 1
    assert (tmp_path / "foo_0.txt").read_bytes() == b"STARThelloEND"

def test_carver_from_file(tmp_path):
    sigs = {"foo": (b"AA", b"BB", ".bin")}
    src = tmp_path / "src.bin"
    src.write_bytes(b"junkAAbbbBBtail")
    carver = Carver("foo", sigs, output_dir=str(tmp_path / "out"))
    count = carver.carve_from_file(str(src))
    assert count == 1
    assert (tmp_path / "out" / "foo_0.bin").read_bytes() == b"AAbbbBBtail"

def test_carver_invalid_key(tmp_path):
    with pytest.raises(ValueError):
        Carver("missing", {}, output_dir=str(tmp_path))

class DummyStream:
    def __init__(self):
        self.parts = [b"X", b"Y", b"ZDATAEND"]
    def read(self, n=-1):
        return self.parts.pop(0) if self.parts else b""

def test_carver_buffer_retain(tmp_path):
    sigs = {"foo": (b"XYZ", b"END", ".bin")}
    carver = Carver("foo", sigs, output_dir=str(tmp_path), sector_size=1)
    count = carver.carve_from_stream(DummyStream())
    assert count == 1
    assert (tmp_path / "foo_0.bin").read_bytes() == b"XYZDATAEND"
