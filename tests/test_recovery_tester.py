import logging
from unittest.mock import MagicMock, patch
import types

import drivehound.recovery_tester as rt


def test_display_ascii_art(capsys):
    rt.display_ascii_art(scale=1, color="red")
    out = capsys.readouterr().out
    assert out.strip() != ""


def test_color_formatter():
    formatter = rt.ColorFormatter("%(message)s")
    record = logging.LogRecord(name="x", level=logging.INFO, pathname=__file__, lineno=1, msg="Found file", args=None, exc_info=None)
    colored = formatter.format(record)
    assert "\033[" in colored


def test_setup_logging(monkeypatch):
    logger = logging.getLogger()
    logger.handlers.clear()
    monkeypatch.setattr(rt.logging, "getLogger", lambda: logger)
    rt.setup_logging()
    assert len(logger.handlers) == 2
    logger.handlers.clear()


@patch("drivehound.recovery_tester.Hound")
@patch("drivehound.recovery_tester.input", side_effect=["1", "y"])
@patch("drivehound.recovery_tester.list_partitions", return_value=["/dev/sda1"])
def test_main(mock_list, mock_input, mock_hound, capsys):
    mock_inst = MagicMock()
    mock_hound.return_value = mock_inst
    mock_inst.recover_files.return_value = {"foo": 1}
    rt.main()
    output = capsys.readouterr().out
    assert "RECOVERY" in output.upper()
    mock_inst.recover_files.assert_called_once()
