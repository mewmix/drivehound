import io
import types
from unittest.mock import MagicMock
import pytest
import drivehound.win_drive_tools as wdt

def test_ascii_hex_converter_roundtrip():
    assert wdt.ascii_hex_converter("Hello") == "48656c6c6f"
    assert wdt.ascii_hex_converter("4142") == "AB"


def test_binary_to_hex():
    assert wdt.binary_to_hex(b"\x00\xff") == "00ff"


def test_open_drive_with_file(tmp_path):
    path = tmp_path / "f.bin"
    path.write_bytes(b"abc")
    with wdt.open_drive(str(path), sector_size=1, chunk_size=4) as reader:
        chunk = reader.read_chunk()
        assert chunk == b"abc"
        assert reader.position == 3


def test_open_drive_drive_letter(monkeypatch):
    m = MagicMock()
    monkeypatch.setattr(wdt, "open_windows_partition", MagicMock(return_value=m))
    result = wdt.open_drive("C:", mode="rb")
    wdt.open_windows_partition.assert_called_once_with("C:", mode="rb")
    assert result is m


def test_list_partitions_posix(monkeypatch):
    fake_os = types.SimpleNamespace(name="posix")
    monkeypatch.setattr(wdt, "os", fake_os)
    output = "Filesystem\n/dev/sda1 1 1 1 1 /\n/dev/sda2 1 1 1 1 /home\n"
    monkeypatch.setattr(wdt.subprocess, "check_output", lambda *a, **kw: output.encode())
    parts = wdt.list_partitions()
    assert parts == ["/dev/sda1", "/dev/sda2"]


def test_list_partitions_windows(monkeypatch):
    fake_os = types.SimpleNamespace(name="nt")
    monkeypatch.setattr(wdt, "os", fake_os)
    output = "Name\nC:\nD:\n"
    monkeypatch.setattr(wdt.subprocess, "check_output", lambda *a, **kw: output.encode())
    parts = wdt.list_partitions()
    assert parts == ["C:", "D:"]
