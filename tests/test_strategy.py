import math
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategy import (  # noqa: E402
    COLUMN_WIN_PROBABILITY,
    break_even_probability_for_2_to_1,
    column_expected_value_units,
)


def test_column_probability_is_12_out_of_37():
    assert math.isclose(COLUMN_WIN_PROBABILITY, 12 / 37)


def test_column_expected_value_is_negative_house_edge():
    assert math.isclose(column_expected_value_units(), -1 / 37)


def test_break_even_probability_for_2_to_1_is_one_third():
    assert math.isclose(break_even_probability_for_2_to_1(), 1 / 3)

