from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List

import numpy as np
import pandas as pd

from strategy import COLUMN_WIN_PROBABILITY, RouletteConfig, fibonacci_sequence


def simulate_fibonacci_session(
    config: RouletteConfig,
    rng: np.random.Generator,
) -> pd.DataFrame:
    bankroll_units = config.starting_bankroll_units
    sequence = fibonacci_sequence(config.table_max_units)
    sequence_index = 0
    peak_bankroll = bankroll_units
    max_drawdown = 0

    rows: List[Dict[str, float]] = []

    for spin in range(1, config.spins + 1):
        requested_bet_units = sequence[sequence_index]
        bet_units = min(requested_bet_units, config.table_max_units, bankroll_units)

        if bet_units <= 0:
            if config.stop_after_ruin:
                break
            rows.append(
                {
                    "spin": spin,
                    "bet_units": 0,
                    "win": False,
                    "profit_units": 0,
                    "bankroll_units": bankroll_units,
                    "drawdown_units": max_drawdown,
                    "sequence_index": sequence_index,
                }
            )
            continue

        win = rng.random() < COLUMN_WIN_PROBABILITY

        if win:
            profit_units = 2 * bet_units
            bankroll_units += profit_units
            sequence_index = 0
        else:
            profit_units = -bet_units
            bankroll_units += profit_units
            sequence_index = min(sequence_index + 1, len(sequence) - 1)

        peak_bankroll = max(peak_bankroll, bankroll_units)
        max_drawdown = max(max_drawdown, peak_bankroll - bankroll_units)

        rows.append(
            {
                "spin": spin,
                "bet_units": bet_units,
                "win": win,
                "profit_units": profit_units,
                "bankroll_units": bankroll_units,
                "drawdown_units": max_drawdown,
                "sequence_index": sequence_index,
            }
        )

        if bankroll_units <= 0 and config.stop_after_ruin:
            break

    return pd.DataFrame(rows)


def simulate_fibonacci_with_max_recovery_session(
    config: RouletteConfig,
    rng: np.random.Generator,
) -> pd.DataFrame:
    bankroll_units = config.starting_bankroll_units
    sequence = fibonacci_sequence(config.table_max_units)
    sequence_index = 0
    in_max_recovery = False
    peak_bankroll = bankroll_units
    max_drawdown = 0

    rows: List[Dict[str, float]] = []

    for spin in range(1, config.spins + 1):
        if not in_max_recovery and sequence[sequence_index] > config.table_max_units:
            in_max_recovery = True

        requested_bet_units = (
            config.table_max_units if in_max_recovery else sequence[sequence_index]
        )
        bet_units = min(requested_bet_units, config.table_max_units, bankroll_units)
        recovery_mode_for_spin = in_max_recovery

        if bet_units <= 0:
            if config.stop_after_ruin:
                break
            rows.append(
                {
                    "spin": spin,
                    "bet_units": 0,
                    "win": False,
                    "profit_units": 0,
                    "bankroll_units": bankroll_units,
                    "drawdown_units": max_drawdown,
                    "sequence_index": sequence_index,
                    "max_recovery_mode": recovery_mode_for_spin,
                }
            )
            continue

        win = rng.random() < COLUMN_WIN_PROBABILITY

        if win:
            profit_units = 2 * bet_units
            bankroll_units += profit_units
            if in_max_recovery and bankroll_units > config.starting_bankroll_units:
                in_max_recovery = False
                sequence_index = 0
            elif in_max_recovery:
                sequence_index = len(sequence) - 1
            else:
                sequence_index = 0
        else:
            profit_units = -bet_units
            bankroll_units += profit_units
            if in_max_recovery:
                sequence_index = len(sequence) - 1
            else:
                sequence_index = min(sequence_index + 1, len(sequence) - 1)

        peak_bankroll = max(peak_bankroll, bankroll_units)
        max_drawdown = max(max_drawdown, peak_bankroll - bankroll_units)

        rows.append(
            {
                "spin": spin,
                "bet_units": bet_units,
                "win": win,
                "profit_units": profit_units,
                "bankroll_units": bankroll_units,
                "drawdown_units": max_drawdown,
                "sequence_index": sequence_index,
                "max_recovery_mode": recovery_mode_for_spin,
            }
        )

        if bankroll_units <= 0 and config.stop_after_ruin:
            break

    return pd.DataFrame(rows)


def simulate_flat_vs_fibonacci_session(
    config: RouletteConfig,
    rng: np.random.Generator,
) -> pd.DataFrame:
    flat_bankroll_units = config.starting_bankroll_units
    fibonacci_bankroll_units = config.starting_bankroll_units
    sequence = fibonacci_sequence(config.table_max_units)
    sequence_index = 0

    flat_peak_bankroll = flat_bankroll_units
    fibonacci_peak_bankroll = fibonacci_bankroll_units
    flat_max_drawdown = 0
    fibonacci_max_drawdown = 0

    rows: List[Dict[str, float]] = []

    for spin in range(1, config.spins + 1):
        win = rng.random() < COLUMN_WIN_PROBABILITY

        flat_bet_units = min(1, flat_bankroll_units)
        if flat_bet_units > 0:
            flat_profit_units = 2 * flat_bet_units if win else -flat_bet_units
            flat_bankroll_units += flat_profit_units
        else:
            flat_profit_units = 0

        fibonacci_bet_units = min(
            sequence[sequence_index],
            config.table_max_units,
            fibonacci_bankroll_units,
        )
        if fibonacci_bet_units > 0:
            if win:
                fibonacci_profit_units = 2 * fibonacci_bet_units
                fibonacci_bankroll_units += fibonacci_profit_units
                sequence_index = 0
            else:
                fibonacci_profit_units = -fibonacci_bet_units
                fibonacci_bankroll_units += fibonacci_profit_units
                sequence_index = min(sequence_index + 1, len(sequence) - 1)
        else:
            fibonacci_profit_units = 0

        flat_peak_bankroll = max(flat_peak_bankroll, flat_bankroll_units)
        fibonacci_peak_bankroll = max(fibonacci_peak_bankroll, fibonacci_bankroll_units)
        flat_max_drawdown = max(flat_max_drawdown, flat_peak_bankroll - flat_bankroll_units)
        fibonacci_max_drawdown = max(
            fibonacci_max_drawdown,
            fibonacci_peak_bankroll - fibonacci_bankroll_units,
        )

        rows.append(
            {
                "spin": spin,
                "win": win,
                "flat_bet_units": flat_bet_units,
                "fibonacci_bet_units": fibonacci_bet_units,
                "flat_profit_units": flat_profit_units,
                "fibonacci_profit_units": fibonacci_profit_units,
                "flat_bankroll_units": flat_bankroll_units,
                "fibonacci_bankroll_units": fibonacci_bankroll_units,
                "flat_drawdown_units": flat_max_drawdown,
                "fibonacci_drawdown_units": fibonacci_max_drawdown,
                "fibonacci_sequence_index": sequence_index,
            }
        )

        if (
            config.stop_after_ruin
            and flat_bankroll_units <= 0
            and fibonacci_bankroll_units <= 0
        ):
            break

    return pd.DataFrame(rows)


def simulate_flat_session(
    config: RouletteConfig,
    rng: np.random.Generator,
) -> pd.DataFrame:
    bankroll_units = config.starting_bankroll_units
    peak_bankroll = bankroll_units
    max_drawdown = 0
    rows: List[Dict[str, float]] = []

    for spin in range(1, config.spins + 1):
        bet_units = min(1, bankroll_units)

        if bet_units <= 0:
            if config.stop_after_ruin:
                break
            profit_units = 0
            win = False
        else:
            win = rng.random() < COLUMN_WIN_PROBABILITY
            profit_units = 2 * bet_units if win else -bet_units
            bankroll_units += profit_units

        peak_bankroll = max(peak_bankroll, bankroll_units)
        max_drawdown = max(max_drawdown, peak_bankroll - bankroll_units)

        rows.append(
            {
                "spin": spin,
                "bet_units": bet_units,
                "win": win,
                "profit_units": profit_units,
                "bankroll_units": bankroll_units,
                "drawdown_units": max_drawdown,
            }
        )

        if bankroll_units <= 0 and config.stop_after_ruin:
            break

    return pd.DataFrame(rows)


def run_monte_carlo(
    sessions: int = 10000,
    seed: int = 42,
    config: RouletteConfig | None = None,
) -> pd.DataFrame:
    config = config or RouletteConfig()
    rng = np.random.default_rng(seed)
    results = []

    for session_id in range(1, sessions + 1):
        session = simulate_fibonacci_session(config, rng)

        if session.empty:
            final_bankroll_units = config.starting_bankroll_units
            max_drawdown_units = 0
            spins_played = 0
        else:
            final_bankroll_units = int(session["bankroll_units"].iloc[-1])
            max_drawdown_units = int(session["drawdown_units"].max())
            spins_played = int(session["spin"].iloc[-1])

        results.append(
            {
                "session_id": session_id,
                "final_bankroll_units": final_bankroll_units,
                "final_profit_units": final_bankroll_units - config.starting_bankroll_units,
                "final_profit": (final_bankroll_units - config.starting_bankroll_units)
                * config.unit_size,
                "max_drawdown_units": max_drawdown_units,
                "max_drawdown": max_drawdown_units * config.unit_size,
                "ruined": final_bankroll_units <= 0,
                "spins_played": spins_played,
                **asdict(config),
            }
        )

    return pd.DataFrame(results)


if __name__ == "__main__":
    results_df = run_monte_carlo()
    results_df.to_csv("outputs/monte_carlo_results.csv", index=False)
    print(results_df.describe(include="all"))
