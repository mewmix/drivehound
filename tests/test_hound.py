import pytest
import platform
from unittest.mock import patch, MagicMock
from drivehound.hound import Hound
import drivehound.win_drive_tools  # Import the module instead of individual functions

@pytest.fixture
def hound():
    """Fixture to initialize Hound instance."""
    return Hound()

def test_hound_init(hound):
    """Ensure Hound initializes properly with default parameters."""
    assert isinstance(hound.signatures, dict)
    assert hound.output_dir == "recovered_files"
    assert hound.sector_size == 512
    assert hound.chunk_size == 512 * 1024  # 524288

@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific test")
@patch("drivehound.win_drive_tools.list_partitions", return_value=["C:", "D:", "E:", "M:", "Z:"])
def test_windows_list_partitions(mock_list_partitions):
    """Mock Windows partition listing."""
    partitions = drivehound.win_drive_tools.list_partitions()
    assert isinstance(partitions, list)
    assert len(partitions) >= 2  # Ensure at least 2 partitions exist
    mock_list_partitions.assert_called_once()

@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific test")
@patch("drivehound.win_drive_tools.open_drive")
@patch("drivehound.win_drive_tools.list_partitions", return_value=["C:", "D:", "E:", "M:", "Z:"])
def test_windows_open_drive(mock_list_partitions, mock_open_drive):
    """Mock Windows drive opening."""
    # Configure the mock to act as a context manager and return a mock reader
    mock_reader = MagicMock()
    mock_reader.read.return_value = b"dummy data"  # Example data
    mock_open_drive.return_value.__enter__.return_value = mock_reader

    partitions = drivehound.win_drive_tools.list_partitions()
    assert isinstance(partitions, list)
    assert len(partitions) >= 1  # Ensure at least one partition exists

    drive = partitions[0]
    with drivehound.win_drive_tools.open_drive(drive, mode="rb") as f:
        assert f is not None
        data = f.read()  # Example read operation
        assert data == b"dummy data"

    mock_list_partitions.assert_called_once()
    mock_open_drive.assert_called_once_with(drive, mode="rb")

@pytest.mark.skipif(platform.system() == "Windows", reason="POSIX-specific test")
@patch("drivehound.win_drive_tools.list_partitions", return_value=["/dev/sda1"])
def test_posix_list_partitions(mock_list_partitions):
    """Mock POSIX partition listing."""
    partitions = drivehound.win_drive_tools.list_partitions()
    assert isinstance(partitions, list)
    assert len(partitions) >= 1
    mock_list_partitions.assert_called_once()

@pytest.mark.skipif(platform.system() == "Windows", reason="POSIX-specific test")
@patch("drivehound.win_drive_tools.open_drive")
@patch("drivehound.win_drive_tools.list_partitions", return_value=["/dev/sda1"])
def test_posix_open_drive(mock_list_partitions, mock_open_drive):
    """Mock POSIX drive opening."""
    # Configure the mock to act as a context manager and return a mock reader
    mock_reader = MagicMock()
    mock_reader.read.return_value = b"dummy data"  # Example data
    mock_open_drive.return_value.__enter__.return_value = mock_reader

    partitions = drivehound.win_drive_tools.list_partitions()
    assert isinstance(partitions, list)
    assert len(partitions) >= 1

    drive = partitions[0]
    with drivehound.win_drive_tools.open_drive(drive, "rb") as f:
        assert f is not None
        data = f.read()  # Example read operation
        assert data == b"dummy data"

    mock_list_partitions.assert_called_once()
    mock_open_drive.assert_called_once_with(drive, "rb")

@patch("drivehound.hound.open_drive")
def test_hound_recover_files_mocked(mock_open_drive, hound, tmp_path):
    """Mock test to ensure Hound can process a dummy file without real disk access."""
    dummy_drive = tmp_path / "dummy_drive.img"
    dummy_drive.write_bytes(b"\x00" * 1024 * 1024)  # Create 1MB empty file

    # Configure the mock to act as a context manager and return a mock reader
    mock_reader = MagicMock()
    # Simulate EOF by returning empty bytes on first read_chunk
    mock_reader.read_chunk.side_effect = [b'']
    mock_open_drive.return_value.__enter__.return_value = mock_reader

    recovered_files = hound.recover_files(str(dummy_drive))
    assert isinstance(recovered_files, dict)
    assert recovered_files == {}  # No actual data, so should be empty

    # Updated assertion to include sector_size and chunk_size
    mock_open_drive.assert_called_once_with(
        str(dummy_drive), 
        mode="rb", 
        sector_size=hound.sector_size, 
        chunk_size=hound.chunk_size
    )
    mock_reader.read_chunk.assert_called_once()
