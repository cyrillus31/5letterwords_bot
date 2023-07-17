import sys

import pytest

sys.path.append("src")

from src import util


@pytest.mark.parametrize("symbol, result", [
    ("Я", True),
    ("", False),
    (123, False),
    ("_", False),
    ("T", False),
    ("Т", True)
])
def test_is_letter(symbol, result):
    assert util.is_letter(symbol) == result


@pytest.mark.parametrize("message, result", [
    ("як0рь", True),
    ("машина", False),
    ("вреmя", True),
    ("smart", False),
    ("T", False)
])
def test_is_valid_string(message, result):
    assert util.is_valid_string(message) == result