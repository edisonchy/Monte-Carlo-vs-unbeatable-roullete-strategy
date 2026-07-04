import math
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategy import (  # noqa: E402
    COLUMN_WIN_PROBABILITY,
    RouletteConfig,
    american_bet_type_rows,
    break_even_probability_for_2_to_1,
    column_expected_value_units,
)
from simulate import (  # noqa: E402
    simulate_fibonacci_with_max_recovery_session,
    simulate_flat_vs_fibonacci_session,
)

import numpy as np


class FixedRng:
    def __init__(self, values):
        self.values = iter(values)

    def random(self):
        return next(self.values)


def test_column_probability_is_12_out_of_38():
    assert math.isclose(COLUMN_WIN_PROBABILITY, 12 / 38)


def test_column_expected_value_is_negative_house_edge():
    assert math.isclose(column_expected_value_units(), -2 / 38)


def test_break_even_probability_for_2_to_1_is_one_third():
    assert math.isclose(break_even_probability_for_2_to_1(), 1 / 3)


def test_most_american_bet_types_have_same_house_edge():
    rows = american_bet_type_rows()
    standard_rows = [row for row in rows if row["name"] != "Five-number bet"]

    for row in standard_rows:
        assert math.isclose(row["ev_units"], -2 / 38)


def test_american_five_number_bet_has_worse_house_edge():
    five_number_bet = next(row for row in american_bet_type_rows() if row["name"] == "Five-number bet")

    assert math.isclose(five_number_bet["ev_units"], -3 / 38)


def test_flat_and_fibonacci_comparison_uses_same_outcomes():
    config = RouletteConfig(spins=25)
    rng = np.random.default_rng(7)

    session = simulate_flat_vs_fibonacci_session(config, rng)

    assert len(session) == 25
    assert set(session["win"].unique()).issubset({True, False})


def test_1000_bankroll_cannot_reach_max_recovery_after_initial_loss_streak():
    config = RouletteConfig(spins=20)
    rng = FixedRng([1.0] * 20)

    session = simulate_fibonacci_with_max_recovery_session(config, rng)

    assert session["bankroll_units"].iloc[-1] == 0
    assert not session["max_recovery_mode"].any()


def test_max_recovery_uses_table_max_after_fibonacci_cap():
    config = RouletteConfig(starting_bankroll=3000, spins=12)
    rng = FixedRng([1.0] * 12)

    session = simulate_fibonacci_with_max_recovery_session(config, rng)

    final_spin = session.iloc[-1]
    assert final_spin["max_recovery_mode"]
    assert final_spin["bet_units"] == config.table_max_units


def test_max_recovery_continues_until_session_profit():
    config = RouletteConfig(starting_bankroll=3000, spins=14)
    rng = FixedRng(([1.0] * 11) + [0.0, 0.0, 1.0])

    session = simulate_fibonacci_with_max_recovery_session(config, rng)

    assert session.loc[session["spin"].eq(12), "max_recovery_mode"].item()
    assert session.loc[session["spin"].eq(13), "max_recovery_mode"].item()
    assert not session.loc[session["spin"].eq(14), "max_recovery_mode"].item()
    assert session.loc[session["spin"].eq(14), "bet_units"].item() == 1
