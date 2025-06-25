import pytest
from drivehound.color_utils import (
    hex_to_rgb,
    rgb_to_ansi_fg,
    rgb_to_ansi_bg,
    colored_text,
    colored_bg_text,
    print_colored,
    print_colored_bg,
)


def test_hex_to_rgb_valid():
    assert hex_to_rgb("#FFAABB") == (255, 170, 187)


def test_hex_to_rgb_invalid():
    with pytest.raises(ValueError):
        hex_to_rgb("#FFF")


def test_rgb_to_ansi_codes():
    assert rgb_to_ansi_fg(1, 2, 3) == "\033[38;2;1;2;3m"
    assert rgb_to_ansi_bg(1, 2, 3) == "\033[48;2;1;2;3m"


def test_colored_text_and_bg_with_hex():
    txt = colored_text("hello", "#00FF00")
    assert "hello" in txt and "\033[" in txt
    bg = colored_bg_text("hello", "#00FF00")
    assert "hello" in bg and "\033[" in bg


def test_print_functions(capsys):
    print_colored("msg", "red")
    print_colored_bg("msg", "blue")
    captured = capsys.readouterr().out
    assert "msg" in captured
