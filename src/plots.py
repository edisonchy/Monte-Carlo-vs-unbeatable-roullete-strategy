from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from simulate import run_monte_carlo, simulate_fibonacci_session
from strategy import (
    COLUMN_POCKETS,
    COLUMN_WIN_PROBABILITY,
    EUROPEAN_ROULETTE_POCKETS,
    RouletteConfig,
    break_even_probability_for_2_to_1,
    column_expected_value_units,
)


sns.set_theme(style="whitegrid")


def save_probability_plot(path: str = "outputs/column_probability.png") -> None:
    losing_pockets = EUROPEAN_ROULETTE_POCKETS - COLUMN_POCKETS
    data = pd.DataFrame(
        {
            "Outcome": ["Chosen column wins", "Chosen column loses"],
            "Pockets": [COLUMN_POCKETS, losing_pockets],
            "Probability": [COLUMN_WIN_PROBABILITY, losing_pockets / EUROPEAN_ROULETTE_POCKETS],
        }
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=data, x="Outcome", y="Probability", hue="Outcome", ax=ax, legend=False)
    ax.set_title("Column Bet Probability on European Roulette")
    ax.set_xlabel("")
    ax.set_ylabel("Probability")
    ax.set_ylim(0, 0.75)

    for index, row in data.iterrows():
        ax.text(
            index,
            row["Probability"] + 0.02,
            f'{row["Pockets"]} pockets\n{row["Probability"]:.2%}',
            ha="center",
            va="bottom",
        )

    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_ev_contribution_plot(path: str = "outputs/expected_value.png") -> None:
    win_contribution = COLUMN_WIN_PROBABILITY * 2
    loss_contribution = (1 - COLUMN_WIN_PROBABILITY) * -1
    net_ev = column_expected_value_units()

    data = pd.DataFrame(
        {
            "Component": ["Win contribution", "Loss contribution", "Net EV"],
            "Units": [win_contribution, loss_contribution, net_ev],
        }
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#2f7d32", "#b3261e", "#333333"]
    ax.bar(data["Component"], data["Units"], color=colors)
    ax.axhline(0, color="black", linewidth=1)
    ax.set_title("Expected Value of a 1-Unit Column Bet")
    ax.set_xlabel("")
    ax.set_ylabel("Expected units per bet")

    for index, row in data.iterrows():
        y = row["Units"]
        va = "bottom" if y >= 0 else "top"
        offset = 0.025 if y >= 0 else -0.025
        ax.text(index, y + offset, f'{y:+.4f}', ha="center", va=va)

    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_break_even_plot(path: str = "outputs/breakeven_vs_actual.png") -> None:
    data = pd.DataFrame(
        {
            "Probability": ["Fair 2:1 break-even", "European roulette column"],
            "Value": [break_even_probability_for_2_to_1(), COLUMN_WIN_PROBABILITY],
        }
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=data, x="Probability", y="Value", hue="Probability", ax=ax, legend=False)
    ax.set_title("Actual Win Probability Is Below Break-Even")
    ax.set_xlabel("")
    ax.set_ylabel("Win probability")
    ax.set_ylim(0.31, 0.34)

    for index, row in data.iterrows():
        ax.text(index, row["Value"] + 0.001, f'{row["Value"]:.2%}', ha="center")

    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_profit_distribution_plot(
    results: pd.DataFrame,
    path: str = "outputs/final_profit_distribution.png",
) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(results["final_profit"], bins=60, kde=True, ax=ax)
    ax.axvline(0, color="black", linewidth=1)
    ax.set_title("Monte Carlo Final Profit Distribution")
    ax.set_xlabel("Final profit")
    ax.set_ylabel("Session count")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_single_bankroll_path(path: str = "outputs/single_bankroll_path.png") -> None:
    config = RouletteConfig()
    rng = __import__("numpy").random.default_rng(7)
    session = simulate_fibonacci_session(config, rng)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(session["spin"], session["bankroll_units"] * config.unit_size)
    ax.axhline(config.starting_bankroll, color="black", linewidth=1)
    ax.set_title("Example Fibonacci Strategy Bankroll Path")
    ax.set_xlabel("Spin")
    ax.set_ylabel("Bankroll")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def generate_all_plots() -> None:
    save_probability_plot()
    save_ev_contribution_plot()
    save_break_even_plot()
    save_single_bankroll_path()

    results = run_monte_carlo(sessions=10000)
    results.to_csv("outputs/monte_carlo_results.csv", index=False)
    save_profit_distribution_plot(results)


if __name__ == "__main__":
    generate_all_plots()

