from dataclasses import dataclass
from typing import Dict, List


EUROPEAN_ROULETTE_POCKETS = 37
AMERICAN_ROULETTE_POCKETS = 38
COLUMN_POCKETS = 12
COLUMN_WIN_PROBABILITY = COLUMN_POCKETS / AMERICAN_ROULETTE_POCKETS

AMERICAN_BET_TYPES = [
    {"name": "Straight up", "numbers_covered": 1, "payout": 35},
    {"name": "Split", "numbers_covered": 2, "payout": 17},
    {"name": "Street / Trio", "numbers_covered": 3, "payout": 11},
    {"name": "Corner", "numbers_covered": 4, "payout": 8},
    {"name": "Five-number bet", "numbers_covered": 5, "payout": 6},
    {"name": "Six line", "numbers_covered": 6, "payout": 5},
    {"name": "Dozen", "numbers_covered": 12, "payout": 2},
    {"name": "Column", "numbers_covered": 12, "payout": 2},
    {"name": "Even-money", "numbers_covered": 18, "payout": 1},
]


@dataclass(frozen=True)
class RouletteConfig:
    starting_bankroll: float = 1000.0
    unit_size: float = 5.0
    table_max: float = 500.0
    spins: int = 500
    stop_after_ruin: bool = True

    @property
    def table_max_units(self) -> int:
        return int(self.table_max // self.unit_size)

    @property
    def starting_bankroll_units(self) -> int:
        return int(self.starting_bankroll // self.unit_size)


def fibonacci_sequence(max_units: int) -> List[int]:
    sequence = [1, 1]
    while sequence[-1] < max_units:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence


def column_expected_value_units() -> float:
    win_probability = COLUMN_WIN_PROBABILITY
    loss_probability = 1 - win_probability
    return (win_probability * 2) + (loss_probability * -1)


def break_even_probability_for_2_to_1() -> float:
    return 1 / 3


def expected_value_units(numbers_covered: int, payout: int, pockets: int) -> float:
    win_probability = numbers_covered / pockets
    loss_probability = 1 - win_probability
    return (win_probability * payout) - loss_probability


def american_bet_type_rows() -> List[Dict[str, float]]:
    rows = []
    for bet in AMERICAN_BET_TYPES:
        win_probability = bet["numbers_covered"] / AMERICAN_ROULETTE_POCKETS
        ev_units = expected_value_units(
            bet["numbers_covered"],
            bet["payout"],
            AMERICAN_ROULETTE_POCKETS,
        )
        rows.append(
            {
                **bet,
                "win_probability": win_probability,
                "loss_probability": 1 - win_probability,
                "ev_units": ev_units,
                "house_edge": -ev_units,
            }
        )
    return rows
