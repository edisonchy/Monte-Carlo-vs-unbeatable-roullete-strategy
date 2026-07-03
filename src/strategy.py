from dataclasses import dataclass
from typing import List


EUROPEAN_ROULETTE_POCKETS = 37
COLUMN_POCKETS = 12
COLUMN_WIN_PROBABILITY = COLUMN_POCKETS / EUROPEAN_ROULETTE_POCKETS


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

