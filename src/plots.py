from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from simulate import (
    run_monte_carlo,
    simulate_fibonacci_with_max_recovery_session,
    simulate_fibonacci_session,
    simulate_flat_session,
    simulate_flat_vs_fibonacci_session,
)
from strategy import (
    AMERICAN_ROULETTE_POCKETS,
    COLUMN_POCKETS,
    COLUMN_WIN_PROBABILITY,
    RouletteConfig,
    american_bet_type_rows,
    break_even_probability_for_2_to_1,
    column_expected_value_units,
)


sns.set_theme(style="whitegrid")


def save_probability_plot(path: str = "outputs/column_probability.png") -> None:
    losing_pockets = AMERICAN_ROULETTE_POCKETS - COLUMN_POCKETS
    data = pd.DataFrame(
        {
            "Outcome": ["Chosen column wins", "Chosen column loses"],
            "Pockets": [COLUMN_POCKETS, losing_pockets],
            "Probability": [COLUMN_WIN_PROBABILITY, losing_pockets / AMERICAN_ROULETTE_POCKETS],
        }
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=data, x="Outcome", y="Probability", hue="Outcome", ax=ax, legend=False)
    ax.set_title("Column Bet Probability on American Roulette")
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


def save_flat_vs_fibonacci_comparison_plot(
    path: str = "outputs/flat_vs_fibonacci_bankroll_path.png",
) -> None:
    config = RouletteConfig(spins=120)
    rng = np.random.default_rng(7)
    session = simulate_flat_vs_fibonacci_session(config, rng)

    session["flat_bankroll"] = session["flat_bankroll_units"] * config.unit_size
    session["fibonacci_bankroll"] = session["fibonacci_bankroll_units"] * config.unit_size

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(
        session["spin"],
        session["flat_bankroll"],
        label="Flat 1-unit betting",
        color="#2f5f8f",
        linewidth=2,
    )
    ax.plot(
        session["spin"],
        session["fibonacci_bankroll"],
        label="Fibonacci betting",
        color="#b3261e",
        linewidth=2,
    )
    ax.axhline(
        config.starting_bankroll,
        color="black",
        linestyle=":",
        linewidth=1.5,
        label="Starting bankroll",
    )
    ax.set_title("Single Simulation: Flat Betting vs Fibonacci Betting")
    ax.set_xlabel("Spin")
    ax.set_ylabel("Bankroll ($)")
    ax.legend()
    ax.yaxis.set_major_formatter(lambda value, _: f"${value:,.0f}")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_flat_betting_normal_distribution_plot(
    path: str = "outputs/flat_betting_normal_distribution.png",
    spins: int = 120,
) -> None:
    config = RouletteConfig(spins=spins)
    win_probability = COLUMN_WIN_PROBABILITY
    loss_probability = 1 - win_probability
    return_values = np.array([2, -1])
    probabilities = np.array([win_probability, loss_probability])

    expected_return_units = float(np.sum(return_values * probabilities))
    expected_bankroll = config.starting_bankroll + (
        expected_return_units * spins * config.unit_size
    )
    return_variance_units = float(
        np.sum(probabilities * (return_values - expected_return_units) ** 2)
    )
    session_standard_deviation = (
        np.sqrt(spins * return_variance_units) * config.unit_size
    )

    x_values = np.linspace(
        expected_bankroll - 4 * session_standard_deviation,
        expected_bankroll + 4 * session_standard_deviation,
        500,
    )
    density = (
        1
        / (session_standard_deviation * np.sqrt(2 * np.pi))
        * np.exp(-0.5 * ((x_values - expected_bankroll) / session_standard_deviation) ** 2)
    )

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(x_values, density, color="#2f5f8f", linewidth=2.5)
    ax.fill_between(x_values, density, color="#2f5f8f", alpha=0.18)
    ax.axvline(
        config.starting_bankroll,
        color="black",
        linestyle=":",
        linewidth=2,
        label=f"Starting bankroll = ${config.starting_bankroll:,.0f}",
    )
    ax.axvline(
        expected_bankroll,
        color="#b3261e",
        linestyle="--",
        linewidth=2,
        label=f"Expected bankroll = ${expected_bankroll:,.0f}",
    )
    ax.set_title("Normal Approximation of Flat Betting Outcomes")
    ax.set_xlabel("Final bankroll after 120 spins")
    ax.set_ylabel("Relative likelihood")
    ax.xaxis.set_major_formatter(lambda value, _: f"${value:,.0f}")
    ax.set_yticks([])
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_fibonacci_equity_paths_plot(
    path: str = "outputs/fibonacci_equity_paths.png",
    sessions: int = 1000,
    spins: int = 120,
    seed: int = 42,
) -> None:
    save_equity_paths_plot(
        simulate_session=simulate_fibonacci_session,
        path=path,
        title=f"Fibonacci Strategy Equity Paths ({sessions:,} Simulations)",
        sessions=sessions,
        spins=spins,
        seed=seed,
    )


def save_fibonacci_max_recovery_equity_paths_plot(
    path: str = "outputs/fibonacci_max_recovery_equity_paths.png",
    sessions: int = 1000,
    spins: int = 120,
    seed: int = 42,
) -> None:
    save_equity_paths_plot(
        simulate_session=simulate_fibonacci_with_max_recovery_session,
        path=path,
        title=f"Fibonacci With $500 Recovery Rule ({sessions:,} Simulations)",
        sessions=sessions,
        spins=spins,
        seed=seed,
    )


def save_flat_equity_paths_plot(
    path: str = "outputs/flat_equity_paths.png",
    sessions: int = 1000,
    spins: int = 120,
    seed: int = 42,
) -> None:
    save_equity_paths_plot(
        simulate_session=simulate_flat_session,
        path=path,
        title=f"Flat Betting Equity Paths ({sessions:,} Simulations)",
        sessions=sessions,
        spins=spins,
        seed=seed,
    )


def save_equity_paths_plot(
    simulate_session,
    path: str,
    title: str,
    sessions: int,
    spins: int,
    seed: int,
) -> None:
    config = RouletteConfig(spins=spins)
    rng = np.random.default_rng(seed)

    paths = []
    final_bankrolls = []

    for _ in range(sessions):
        session = simulate_session(config, rng)
        bankroll = np.full(spins + 1, np.nan)
        bankroll[0] = config.starting_bankroll

        if not session.empty:
            played_spins = session["spin"].astype(int).to_numpy()
            bankroll[played_spins] = session["bankroll_units"].to_numpy() * config.unit_size
            final_spin = int(played_spins[-1])
            final_bankroll = bankroll[final_spin]
            if final_spin < spins:
                bankroll[final_spin + 1 :] = final_bankroll
        else:
            final_bankroll = config.starting_bankroll
            bankroll[1:] = final_bankroll

        paths.append(bankroll)
        final_bankrolls.append(final_bankroll)

    x_values = np.arange(spins + 1)
    median_final = float(np.median(final_bankrolls))

    with plt.style.context("dark_background"):
        fig, ax = plt.subplots(figsize=(14, 6))
        fig.patch.set_facecolor("#050505")
        ax.set_facecolor("#050505")

        for bankroll, final_bankroll in zip(paths, final_bankrolls):
            color = "#5ad7a0" if final_bankroll >= config.starting_bankroll else "#ff6f7d"
            ax.plot(x_values, bankroll, color=color, alpha=0.16, linewidth=0.9)

        ax.axhline(
            config.starting_bankroll,
            color="#d7dde4",
            linestyle="--",
            linewidth=1.4,
            alpha=0.9,
            label="Starting bankroll",
        )
        ax.axhline(
            0,
            color="#ff6f7d",
            linestyle="--",
            linewidth=1.4,
            alpha=0.9,
            label="Ruin",
        )

        ax.set_title(
            title,
            loc="left",
            color="#d7dde4",
            fontsize=14,
            pad=14,
        )
        ax.text(
            0,
            1.02,
            f"Spins per session: {spins}    Median final bankroll: ${median_final:,.0f}",
            transform=ax.transAxes,
            color="#9aa0a6",
            fontsize=10,
        )
        ax.set_xlabel("Spin", color="#d7dde4")
        ax.set_ylabel("Bankroll ($)", color="#d7dde4")
        ax.yaxis.set_major_formatter(lambda value, _: f"${value:,.0f}")
        ax.tick_params(colors="#9aa0a6")
        ax.grid(color="#2b3035", linestyle="--", linewidth=0.8, alpha=0.7)
        ax.spines["bottom"].set_color("#2b3035")
        ax.spines["left"].set_color("#2b3035")
        ax.spines["top"].set_color("#2b3035")
        ax.spines["right"].set_color("#2b3035")
        ax.legend(loc="upper right", frameon=False, labelcolor="#d7dde4")
        fig.tight_layout()
        fig.savefig(path, dpi=160, facecolor=fig.get_facecolor())
        plt.close(fig)


def save_american_bet_ev_comparison_plot(
    path: str = "outputs/american_bet_ev_comparison.png",
) -> None:
    data = pd.DataFrame(american_bet_type_rows())
    data["Expected loss"] = data["house_edge"] * 100

    fig, ax = plt.subplots(figsize=(11, 6))
    colors = np.where(data["name"].eq("Five-number bet"), "#b3261e", "#2f5f8f")
    ax.bar(data["name"], data["Expected loss"], color=colors)
    ax.set_title("American Roulette Expected Loss by Bet Type")
    ax.set_xlabel("")
    ax.set_ylabel("Expected loss per unit bet")
    ax.set_ylim(0, 9)
    ax.tick_params(axis="x", rotation=35)

    for index, row in data.iterrows():
        ax.text(
            index,
            row["Expected loss"] + 0.18,
            f'{row["Expected loss"]:.2f}%',
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_american_average_return_over_time_plot(
    bet_name: str,
    path: str,
    title_name: str | None = None,
    color: str = "#1f77b4",
    bets: int = 10000,
    seed: int = 24,
) -> None:
    rng = np.random.default_rng(seed)
    bet_type = next(row for row in american_bet_type_rows() if row["name"] == bet_name)
    wins = rng.random(bets) < bet_type["win_probability"]
    returns = np.where(wins, bet_type["payout"], -1)
    average_return_percentage = np.cumsum(returns) / np.arange(1, bets + 1) * 100
    theoretical_ev_percentage = bet_type["ev_units"] * 100

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(
        np.arange(1, bets + 1),
        average_return_percentage,
        color=color,
        linewidth=2,
        label="Simulated average return",
    )
    ax.axhline(
        theoretical_ev_percentage,
        color=color,
        linestyle="--",
        linewidth=2,
        label=f"Expected value = {theoretical_ev_percentage:.2f}%",
    )
    ax.axhline(
        0,
        color=color,
        linestyle=":",
        linewidth=2,
        label="Break-even = 0%",
    )
    title_name = title_name or bet_name
    ax.set_title(f"American Roulette {title_name}: Average Return Over Time")
    ax.set_xlabel("Number of bets")
    ax.set_ylabel("Average return per bet (%)")
    ax.legend()
    ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0f}%")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_american_ev_convergence_plot(path: str = "outputs/american_ev_convergence.png") -> None:
    save_american_average_return_over_time_plot("Column", path)


def save_requested_average_return_plots() -> None:
    save_american_average_return_over_time_plot(
        "Column",
        "outputs/standard_bets_average_return_over_time.png",
        title_name="Standard Bets",
        color="#1f77b4",
        seed=24,
    )
    save_american_average_return_over_time_plot(
        "Five-number bet",
        "outputs/five_number_bet_average_return_over_time.png",
        color="#b3261e",
        seed=24,
    )


def generate_all_plots() -> None:
    save_probability_plot()
    save_ev_contribution_plot()
    save_break_even_plot()
    save_single_bankroll_path()
    save_flat_betting_normal_distribution_plot()
    save_flat_vs_fibonacci_comparison_plot()
    save_fibonacci_equity_paths_plot()
    save_fibonacci_max_recovery_equity_paths_plot()
    save_flat_equity_paths_plot()
    save_american_bet_ev_comparison_plot()
    save_american_ev_convergence_plot()
    save_requested_average_return_plots()

    results = run_monte_carlo(sessions=10000)
    results.to_csv("outputs/monte_carlo_results.csv", index=False)
    save_profit_distribution_plot(results)


if __name__ == "__main__":
    generate_all_plots()
